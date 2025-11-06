from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.alineacion import Alineacion
from app.services.backend_api_client import BackendAPIClient

alineacion_bp = Blueprint('alineaciones', __name__)

@alineacion_bp.route('', methods=['POST'])
@jwt_required()
def crear_alineacion():
    """Crea una alineación usando NOMBRE del jugador"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data.get('id_partido'):
            return jsonify({'error': 'El partido es requerido'}), 400
        
        if not data.get('id_equipo'):
            return jsonify({'error': 'El equipo es requerido'}), 400
        
        if not data.get('nombre_jugador'):
            return jsonify({'error': 'El nombre del jugador es requerido'}), 400
        
        # Cliente para consultar backend principal
        api_client = BackendAPIClient()
        
        # Validar que el partido existe
        partido = api_client.get_partido(data['id_partido'])
        if not partido:
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        # Validar que el equipo participa en el partido
        if not api_client.validar_equipo_en_partido(data['id_equipo'], data['id_partido']):
            return jsonify({'error': 'El equipo no participa en este partido'}), 400
        
        # Buscar jugador por nombre
        nombre_jugador = data['nombre_jugador'].strip()
        
        # Obtener todos los jugadores del equipo
        try:
            import requests
            response = requests.get(
                f"{api_client.base_url}/jugadores?id_equipo={data['id_equipo']}", 
                timeout=5
            )
            if response.status_code == 200:
                jugadores = response.json().get('jugadores', [])
                
                # Buscar por nombre completo
                jugador = None
                for j in jugadores:
                    nombre_completo = f"{j['nombre']} {j['apellido']}"
                    if nombre_jugador.lower() in nombre_completo.lower():
                        jugador = j
                        break
                
                if not jugador:
                    return jsonify({
                        'error': 'Jugador no encontrado',
                        'mensaje': f'No existe un jugador "{nombre_jugador}" en el equipo'
                    }), 404
                
                id_jugador = jugador['id_jugador']
            else:
                return jsonify({'error': 'No se pudieron obtener los jugadores'}), 500
        except Exception as e:
            return jsonify({'error': f'Error al buscar jugador: {str(e)}'}), 500
        
        # Validar que el jugador no esté ya en la alineación
        alineacion_existente = Alineacion.query.filter_by(
            id_partido=data['id_partido'],
            id_jugador=id_jugador
        ).first()
        
        if alineacion_existente:
            return jsonify({'error': f'{nombre_jugador} ya está en la alineación'}), 400
        
        # Crear alineación
        nueva_alineacion = Alineacion(
            id_partido=data['id_partido'],
            id_equipo=data['id_equipo'],
            id_jugador=id_jugador,
            titular=data.get('titular', True),
            minuto_entrada=data.get('minuto_entrada', 0),
            minuto_salida=data.get('minuto_salida')
        )
        
        db.session.add(nueva_alineacion)
        db.session.commit()
        
        # Enriquecer respuesta
        response = nueva_alineacion.to_dict()
        response['jugador_nombre'] = f"{jugador['nombre']} {jugador['apellido']}"
        response['dorsal'] = jugador['dorsal']
        response['posicion'] = jugador['posicion']
        
        equipo = api_client.get_equipo(data['id_equipo'])
        if equipo:
            response['equipo_nombre'] = equipo['nombre']
        
        return jsonify({
            'mensaje': 'Alineación registrada exitosamente',
            'alineacion': response
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@alineacion_bp.route('', methods=['GET'])
def obtener_alineaciones():
    """Obtiene alineaciones con datos enriquecidos"""
    try:
        id_partido = request.args.get('id_partido')
        id_equipo = request.args.get('id_equipo')
        
        query = Alineacion.query
        
        if id_partido:
            query = query.filter_by(id_partido=int(id_partido))
        
        if id_equipo:
            query = query.filter_by(id_equipo=int(id_equipo))
        
        alineaciones = query.all()
        
        # Enriquecer con datos del backend principal
        api_client = BackendAPIClient()
        resultado = []
        
        for alineacion in alineaciones:
            data = alineacion.to_dict()
            
            # Obtener datos del jugador
            jugador = api_client.get_jugador(alineacion.id_jugador)
            if jugador:
                data['jugador_nombre'] = f"{jugador.get('nombre')} {jugador.get('apellido')}"
                data['dorsal'] = jugador.get('dorsal')
                data['posicion'] = jugador.get('posicion')
            
            # Obtener datos del equipo
            equipo = api_client.get_equipo(alineacion.id_equipo)
            if equipo:
                data['equipo_nombre'] = equipo.get('nombre')
            
            resultado.append(data)
        
        return jsonify({
            'alineaciones': resultado,
            'total': len(resultado)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@alineacion_bp.route('/<int:id_alineacion>', methods=['DELETE'])
@jwt_required()
def eliminar_alineacion(id_alineacion):
    """Elimina una alineación"""
    try:
        alineacion = Alineacion.query.get(id_alineacion)
        
        if not alineacion:
            return jsonify({'error': 'Alineación no encontrada'}), 404
        
        db.session.delete(alineacion)
        db.session.commit()
        
        return jsonify({'mensaje': 'Alineación eliminada'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# NUEVO: DEFINIR ALINEACIÓN COMPLETA
# ============================================
@alineacion_bp.route('/definir-alineacion', methods=['POST'])
@jwt_required()
def definir_alineacion():

    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('id_partido'):
            return jsonify({'error': 'El partido es requerido'}), 400
        
        if not data.get('id_equipo'):
            return jsonify({'error': 'El equipo es requerido'}), 400
        
        if not data.get('titulares') or len(data['titulares']) < 5:
            return jsonify({'error': 'Debes definir al menos 5 titulares'}), 400
        
        api_client = BackendAPIClient()
        
        # Validar partido
        partido = api_client.get_partido(data['id_partido'])
        if not partido:
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        # Validar que el partido esté en estado 'programado'
        if partido.get('estado') != 'programado':
            return jsonify({'error': 'Solo se puede definir alineación en partidos programados'}), 400
        
        # Validar equipo en partido
        if not api_client.validar_equipo_en_partido(data['id_equipo'], data['id_partido']):
            return jsonify({'error': 'El equipo no participa en este partido'}), 400
        
        # Obtener jugadores del equipo
        import requests
        response = requests.get(
            f"{api_client.base_url}/jugadores?id_equipo={data['id_equipo']}", 
            timeout=5
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'No se pudieron obtener los jugadores'}), 500
        
        jugadores_equipo = response.json().get('jugadores', [])
        
        # Limpiar alineaciones previas de este equipo en este partido
        Alineacion.query.filter_by(
            id_partido=data['id_partido'],
            id_equipo=data['id_equipo']
        ).delete()
        
        alineaciones_creadas = []
        errores = []
        
        # Procesar titulares
        for idx, titular in enumerate(data.get('titulares', [])):
            nombre_titular = titular.get('nombre', '').strip()
            
            if not nombre_titular:
                errores.append(f"Titular #{idx+1} sin nombre")
                continue
            
            # Buscar jugador
            jugador = None
            for j in jugadores_equipo:
                nombre_completo = f"{j['nombre']} {j['apellido']}"
                if nombre_titular.lower() in nombre_completo.lower():
                    jugador = j
                    break
            
            if not jugador:
                errores.append(f"Titular '{nombre_titular}' no encontrado")
                continue
            
            nueva_alineacion = Alineacion(
                id_partido=data['id_partido'],
                id_equipo=data['id_equipo'],
                id_jugador=jugador['id_jugador'],
                titular=True,
                minuto_entrada=0
            )
            
            db.session.add(nueva_alineacion)
            alineaciones_creadas.append({
                'nombre': f"{jugador['nombre']} {jugador['apellido']}",
                'dorsal': jugador['dorsal'],
                'posicion': jugador['posicion'],
                'titular': True,
                'minuto_entrada': 0
            })
        
        # Procesar suplentes
        for suplente in data.get('suplentes', []):
            nombre_suplente = suplente.get('nombre', '').strip()
            
            if not nombre_suplente:
                continue
            
            jugador = None
            for j in jugadores_equipo:
                nombre_completo = f"{j['nombre']} {j['apellido']}"
                if nombre_suplente.lower() in nombre_completo.lower():
                    jugador = j
                    break
            
            if not jugador:
                errores.append(f"Suplente '{nombre_suplente}' no encontrado")
                continue
            
            nueva_alineacion = Alineacion(
                id_partido=data['id_partido'],
                id_equipo=data['id_equipo'],
                id_jugador=jugador['id_jugador'],
                titular=False,
                minuto_entrada=None
            )
            
            db.session.add(nueva_alineacion)
            alineaciones_creadas.append({
                'nombre': f"{jugador['nombre']} {jugador['apellido']}",
                'dorsal': jugador['dorsal'],
                'posicion': jugador['posicion'],
                'titular': False
            })
        
        db.session.commit()
        
        return jsonify({
            'mensaje': f'Alineación definida: {len([a for a in alineaciones_creadas if a["titular"]])} titulares, {len([a for a in alineaciones_creadas if not a["titular"]])} suplentes',
            'alineaciones': alineaciones_creadas,
            'errores': errores if errores else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# NUEVO: HACER CAMBIO DURANTE EL PARTIDO
# ============================================
@alineacion_bp.route('/cambio', methods=['POST'])
@jwt_required()
def hacer_cambio():
    """
    Hace un cambio durante el partido: saca un titular, entra un suplente
    
    Body:
    {
        "id_partido": 31,
        "id_equipo": 5,
        "sale": "Fernando Gaibor",
        "entra": "Jonathan Perlaza",
        "minuto": 65
    }
    """
    try:
        data = request.get_json()
        
        # Validaciones
        required = ['id_partido', 'id_equipo', 'sale', 'entra', 'minuto']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        api_client = BackendAPIClient()
        
        # Validar partido
        partido = api_client.get_partido(data['id_partido'])
        if not partido:
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        # Validar que el partido esté en estado 'en_juego'
        if partido.get('estado') != 'en_juego':
            return jsonify({'error': 'Solo se pueden hacer cambios en partidos en juego'}), 400
        
        # Obtener jugadores del equipo
        import requests
        response = requests.get(
            f"{api_client.base_url}/jugadores?id_equipo={data['id_equipo']}", 
            timeout=5
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'No se pudieron obtener los jugadores'}), 500
        
        jugadores_equipo = response.json().get('jugadores', [])
        
        # Buscar jugador que SALE
        jugador_sale = None
        for j in jugadores_equipo:
            nombre_completo = f"{j['nombre']} {j['apellido']}"
            if data['sale'].lower() in nombre_completo.lower():
                jugador_sale = j
                break
        
        if not jugador_sale:
            return jsonify({'error': f'Jugador "{data["sale"]}" no encontrado'}), 404
        
        # Buscar jugador que ENTRA
        jugador_entra = None
        for j in jugadores_equipo:
            nombre_completo = f"{j['nombre']} {j['apellido']}"
            if data['entra'].lower() in nombre_completo.lower():
                jugador_entra = j
                break
        
        if not jugador_entra:
            return jsonify({'error': f'Jugador "{data["entra"]}" no encontrado'}), 404
        
        # Buscar alineación del que SALE
        alineacion_sale = Alineacion.query.filter_by(
            id_partido=data['id_partido'],
            id_equipo=data['id_equipo'],
            id_jugador=jugador_sale['id_jugador']
        ).first()
        
        if not alineacion_sale:
            return jsonify({'error': f'{data["sale"]} no está en la alineación'}), 400
        
        if alineacion_sale.minuto_salida is not None:
            return jsonify({'error': f'{data["sale"]} ya fue sustituido anteriormente'}), 400
        
        # Verificar que el minuto de salida sea mayor que el de entrada
        if alineacion_sale.minuto_entrada is not None and data['minuto'] <= alineacion_sale.minuto_entrada:
            return jsonify({'error': 'El minuto de salida debe ser mayor al de entrada'}), 400
        
        # Buscar alineación del que ENTRA
        alineacion_entra = Alineacion.query.filter_by(
            id_partido=data['id_partido'],
            id_equipo=data['id_equipo'],
            id_jugador=jugador_entra['id_jugador']
        ).first()
        
        if not alineacion_entra:
            return jsonify({'error': f'{data["entra"]} no está en la lista de convocados'}), 400
        
        if alineacion_entra.minuto_entrada is not None:
            return jsonify({'error': f'{data["entra"]} ya está en la cancha'}), 400
        
        # Realizar el cambio
        alineacion_sale.minuto_salida = data['minuto']
        alineacion_entra.minuto_entrada = data['minuto']
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Cambio realizado exitosamente',
            'cambio': {
                'sale': {
                    'nombre': f"{jugador_sale['nombre']} {jugador_sale['apellido']}",
                    'dorsal': jugador_sale['dorsal'],
                    'minuto_salida': data['minuto']
                },
                'entra': {
                    'nombre': f"{jugador_entra['nombre']} {jugador_entra['apellido']}",
                    'dorsal': jugador_entra['dorsal'],
                    'minuto_entrada': data['minuto']
                }
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# NUEVO: AUTO-GENERAR ALINEACIONES (SOLO PARA PRUEBAS RÁPIDAS)
# ============================================
@alineacion_bp.route('/auto-generar', methods=['POST'])
@jwt_required()
def auto_generar_alineaciones():
    """
    Genera automáticamente alineaciones para todos los partidos de un campeonato
    SOLO PARA PRUEBAS - En producción el líder debe definir manualmente
    
    Body:
    {
        "id_campeonato": 2
    }
    """
    try:
        import requests
        data = request.get_json()
        
        if not data.get('id_campeonato'):
            return jsonify({'error': 'El campeonato es requerido'}), 400
        
        id_campeonato = data['id_campeonato']
        api_client = BackendAPIClient()
        
        # Obtener todos los partidos del campeonato
        response = requests.get(
            f"{api_client.base_url}/partido?id_campeonato={id_campeonato}",
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'No se pudieron obtener los partidos'}), 500
        
        partidos = response.json().get('partidos', [])
        
        if not partidos:
            return jsonify({'error': 'No hay partidos en este campeonato'}), 404
        
        alineaciones_creadas = 0
        partidos_procesados = 0
        errores = []
        
        for partido in partidos:
            try:
                id_partido = partido['id_partido']
                id_equipo_local = partido['id_equipo_local']
                id_equipo_visitante = partido['id_equipo_visitante']
                
                # Procesar equipo local
                try:
                    response_local = requests.get(
                        f"{api_client.base_url}/jugadores?id_equipo={id_equipo_local}",
                        timeout=5
                    )
                    
                    if response_local.status_code == 200:
                        jugadores_local = response_local.json().get('jugadores', [])
                        
                        # Primeros 5 titulares, resto suplentes
                        for idx, jugador in enumerate(jugadores_local):
                            existe = Alineacion.query.filter_by(
                                id_partido=id_partido,
                                id_jugador=jugador['id_jugador']
                            ).first()
                            
                            if not existe:
                                nueva_alineacion = Alineacion(
                                    id_partido=id_partido,
                                    id_equipo=id_equipo_local,
                                    id_jugador=jugador['id_jugador'],
                                    titular=(idx < 5),
                                    minuto_entrada=0 if idx < 5 else None
                                )
                                
                                db.session.add(nueva_alineacion)
                                alineaciones_creadas += 1
                except Exception as e:
                    errores.append(f"Partido {id_partido} - Local: {str(e)}")
                
                # Procesar equipo visitante
                try:
                    response_visitante = requests.get(
                        f"{api_client.base_url}/jugadores?id_equipo={id_equipo_visitante}",
                        timeout=5
                    )
                    
                    if response_visitante.status_code == 200:
                        jugadores_visitante = response_visitante.json().get('jugadores', [])
                        
                        for idx, jugador in enumerate(jugadores_visitante):
                            existe = Alineacion.query.filter_by(
                                id_partido=id_partido,
                                id_jugador=jugador['id_jugador']
                            ).first()
                            
                            if not existe:
                                nueva_alineacion = Alineacion(
                                    id_partido=id_partido,
                                    id_equipo=id_equipo_visitante,
                                    id_jugador=jugador['id_jugador'],
                                    titular=(idx < 5),
                                    minuto_entrada=0 if idx < 5 else None
                                )
                                
                                db.session.add(nueva_alineacion)
                                alineaciones_creadas += 1
                except Exception as e:
                    errores.append(f"Partido {id_partido} - Visitante: {str(e)}")
                
                partidos_procesados += 1
                
            except Exception as e:
                errores.append(f"Partido {partido.get('id_partido', '?')}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Alineaciones generadas automáticamente',
            'partidos_procesados': partidos_procesados,
            'alineaciones_creadas': alineaciones_creadas,
            'errores': errores if errores else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================
# BATCH (MANTENER PARA COMPATIBILIDAD)
# ============================================
@alineacion_bp.route('/batch', methods=['POST'])
@jwt_required()
def crear_alineacion_batch():
    """
    Crea múltiples alineaciones de golpe (DEPRECADO - Usar /definir-alineacion)
    """
    try:
        data = request.get_json()
        
        if not data.get('id_partido'):
            return jsonify({'error': 'El partido es requerido'}), 400
        
        if not data.get('id_equipo'):
            return jsonify({'error': 'El equipo es requerido'}), 400
        
        if not data.get('titulares'):
            return jsonify({'error': 'Debes especificar al menos 1 titular'}), 400
        
        api_client = BackendAPIClient()
        
        # Validar partido
        partido = api_client.get_partido(data['id_partido'])
        if not partido:
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        # Validar equipo en partido
        if not api_client.validar_equipo_en_partido(data['id_equipo'], data['id_partido']):
            return jsonify({'error': 'El equipo no participa en este partido'}), 400
        
        # Obtener jugadores del equipo
        import requests
        response = requests.get(
            f"{api_client.base_url}/jugadores?id_equipo={data['id_equipo']}", 
            timeout=5
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'No se pudieron obtener los jugadores'}), 500
        
        jugadores_equipo = response.json().get('jugadores', [])
        
        alineaciones_creadas = []
        errores = []
        
        # Procesar titulares
        for nombre_titular in data.get('titulares', []):
            jugador = None
            for j in jugadores_equipo:
                nombre_completo = f"{j['nombre']} {j['apellido']}"
                if nombre_titular.lower() in nombre_completo.lower():
                    jugador = j
                    break
            
            if not jugador:
                errores.append(f"Titular '{nombre_titular}' no encontrado")
                continue
            
            # Verificar si ya existe
            existe = Alineacion.query.filter_by(
                id_partido=data['id_partido'],
                id_jugador=jugador['id_jugador']
            ).first()
            
            if existe:
                errores.append(f"{nombre_titular} ya está en la alineación")
                continue
            
            nueva_alineacion = Alineacion(
                id_partido=data['id_partido'],
                id_equipo=data['id_equipo'],
                id_jugador=jugador['id_jugador'],
                titular=True,
                minuto_entrada=0
            )
            
            db.session.add(nueva_alineacion)
            alineaciones_creadas.append({
                'nombre': f"{jugador['nombre']} {jugador['apellido']}",
                'dorsal': jugador['dorsal'],
                'posicion': jugador['posicion'],
                'titular': True
            })
        
        # Procesar suplentes
        for nombre_suplente in data.get('suplentes', []):
            jugador = None
            for j in jugadores_equipo:
                nombre_completo = f"{j['nombre']} {j['apellido']}"
                if nombre_suplente.lower() in nombre_completo.lower():
                    jugador = j
                    break
            
            if not jugador:
                errores.append(f"Suplente '{nombre_suplente}' no encontrado")
                continue
            
            existe = Alineacion.query.filter_by(
                id_partido=data['id_partido'],
                id_jugador=jugador['id_jugador']
            ).first()
            
            if existe:
                errores.append(f"{nombre_suplente} ya está en la alineación")
                continue
            
            nueva_alineacion = Alineacion(
                id_partido=data['id_partido'],
                id_equipo=data['id_equipo'],
                id_jugador=jugador['id_jugador'],
                titular=False,
                minuto_entrada=None
            )
            
            db.session.add(nueva_alineacion)
            alineaciones_creadas.append({
                'nombre': f"{jugador['nombre']} {jugador['apellido']}",
                'dorsal': jugador['dorsal'],
                'posicion': jugador['posicion'],
                'titular': False
            })
        
        db.session.commit()
        
        return jsonify({
            'mensaje': f'{len(alineaciones_creadas)} alineaciones creadas',
            'alineaciones': alineaciones_creadas,
            'errores': errores if errores else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500