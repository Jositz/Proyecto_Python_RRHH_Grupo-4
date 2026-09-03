# ==========================================================
# SISTEMA DE GESTION DE RECURSOS HUMANOS - GRUPO 4
# VERSION PYTHON - TRABAJADORES MENSUALES
# ==========================================================



DEDUCIBLE_ANUAL = 40000
TASA_RAP = 0.015
TASA_ISR_1 = 0.12
TASA_ISR_2 = 0.15
TASA_ISR_3 = 0.20
LIMITE_ISR_1 = 120000
LIMITE_ISR_2 = 240000


# ==========================================================
# BUSCAR EMPLEADO POR ID
# ==========================================================

def buscar_empleado(cantidad, ids, id_buscado):
    for i in range(cantidad):
        if ids[i] == id_buscado:
            return i
    return -1


# ==========================================================
# SELECCIONAR EMPLEADO
# ==========================================================

def seleccionar_empleado(cantidad, ids):
    while True:
        try:
            id_buscado = int(input("Ingrese ID del empleado (0 = Cancelar): "))

            if id_buscado == 0:
                return 0

            pos = buscar_empleado(cantidad, ids, id_buscado)

            if pos == -1:
                print("Empleado no encontrado. Intente nuevamente.")
            else:
                return pos

        except ValueError:
            print("Ingrese un ID valido.")


# ==========================================================
# INICIALIZAR DATOS
# ==========================================================

def inicializar_datos():

    ids = [1111, 2222, 3333, 4444, 5555, 6666]

    nombres = [
        "Empleado 1",
        "Empleado 2",
        "Empleado 3",
        "RRHH 1",
        "RRHH 2",
        "Administrador"
    ]

    roles = [
        "EMPLEADO",
        "EMPLEADO",
        "EMPLEADO",
        "RRHH",
        "RRHH",
        "ADMIN"
    ]

    antiguedad = [3, 2, 1, 4, 5, 6]

    dias_vacaciones = [15, 12, 10, 20, 20, 20]

    dias_solicitados = [0] * 6

    salario_mensual = [12000, 10000, 9000, 15000, 16000, 20000]

    estado = ["Sin solicitud"] * 6

    historial = ["Sin movimientos"] * 6

    horas_extra = [0] * 6

    pago_horas_extra = [0] * 6

    # Nuevos datos de planilla
    rap = [0] * 6
    salario_anual = [0] * 6
    deducible_anual = [DEDUCIBLE_ANUAL] * 6
    excedente_anual = [0] * 6
    isr_anual = [0] * 6
    isr_mensual = [0] * 6
    deducciones = [0] * 6

    salario_bruto = salario_mensual.copy()
    salario_neto = salario_mensual.copy()

    pago_registrado = [False] * 6

    return (
        ids, nombres, roles, antiguedad, dias_vacaciones,
        dias_solicitados, salario_mensual, estado, historial,
        horas_extra, pago_horas_extra, rap, salario_anual,
        deducible_anual, excedente_anual, isr_anual, isr_mensual,
        deducciones, salario_bruto, salario_neto, pago_registrado
    )


# ==========================================================
# CALCULAR DIAS DE VACACIONES SEGUN ANTIGUEDAD
# ==========================================================

def calcular_dias_vacaciones(anios):

    if anios < 1:
        return 0
    elif anios == 1:
        return 10
    elif anios == 2:
        return 12
    elif anios == 3:
        return 15
    else:
        return 20


# ==========================================================
# CALCULAR ISR Y RAP
# ==========================================================

def calcular_deducciones(salario_bruto):

    # RAP mensual
    rap_mensual = salario_bruto * TASA_RAP

    # Salario anual
    salario_anual = salario_bruto * 12

    # Deducible anual
    deducible_anual = DEDUCIBLE_ANUAL

    # Excedente anual despues del deducible
    excedente_anual = salario_anual - deducible_anual

    if excedente_anual <= 0:
        excedente_anual = 0
        isr_anual = 0
        tasa_utilizada = 0

    else:
        # Se determina la tasa segun el salario anual
        if salario_anual <= LIMITE_ISR_1:
            tasa_utilizada = TASA_ISR_1

        elif salario_anual <= LIMITE_ISR_2:
            tasa_utilizada = TASA_ISR_2

        else:
            tasa_utilizada = TASA_ISR_3

        isr_anual = excedente_anual * tasa_utilizada

    # Convertir ISR anual a mensual
    isr_mensual = isr_anual / 12

    # Total de deducciones mensuales
    total_deducciones = rap_mensual + isr_mensual

    return (
        rap_mensual,
        salario_anual,
        deducible_anual,
        excedente_anual,
        isr_anual,
        isr_mensual,
        total_deducciones,
        tasa_utilizada
    )


# ==========================================================
# CALCULAR PLANILLA MENSUAL
# ==========================================================

def calcular_pago_mensual(
    pos,
    salario_mensual,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    valor_hora = salario_mensual[pos] / 240

    pago_horas_extra[pos] = (
        horas_extra[pos] * valor_hora * 1.25
    )

    salario_bruto[pos] = (
        salario_mensual[pos] + pago_horas_extra[pos]
    )

    (
        rap[pos],
        salario_anual[pos],
        deducible_anual[pos],
        excedente_anual[pos],
        isr_anual[pos],
        isr_mensual[pos],
        deducciones[pos],
        tasa_utilizada
    ) = calcular_deducciones(salario_bruto[pos])

    salario_neto[pos] = (
        salario_bruto[pos] - deducciones[pos]
    )

    pago_registrado[pos] = True

    return tasa_utilizada


# ==========================================================
# MOSTRAR RECIBO DE PAGO
# ==========================================================

def mostrar_recibo(
    pos,
    ids,
    nombres,
    salario_mensual,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    print("=" * 55)
    print("              RECIBO DE PAGO MENSUAL")
    print("=" * 55)

    print(f"ID: {ids[pos]}")
    print(f"Empleado: {nombres[pos]}")
    print("Modalidad: MENSUAL")
    print(f"Salario mensual: L. {salario_mensual[pos]:,.2f}")

    if pago_registrado[pos]:

        print(f"Horas extra diurnas: {horas_extra[pos]:,.2f}")
        print(f"Pago horas extra: L. {pago_horas_extra[pos]:,.2f}")

        print("-" * 55)
        print(f"Salario bruto: L. {salario_bruto[pos]:,.2f}")
        print(f"RAP (1.5%): L. {rap[pos]:,.2f}")

        print(f"Salario anual proyectado: L. {salario_anual[pos]:,.2f}")
        print(f"Deducible anual: L. {deducible_anual[pos]:,.2f}")
        print(f"Excedente anual: L. {excedente_anual[pos]:,.2f}")
        print(f"ISR anual: L. {isr_anual[pos]:,.2f}")
        print(f"ISR mensual: L. {isr_mensual[pos]:,.2f}")

        print(f"TOTAL DEDUCCIONES: L. {deducciones[pos]:,.2f}")
        print(f"SALARIO NETO: L. {salario_neto[pos]:,.2f}")

    else:
        print("Planilla del mes aun no calculada.")


# ==========================================================
# SOLICITAR VACACIONES
# ==========================================================

def vacaciones(
    pos,
    dias_vacaciones,
    dias_solicitados,
    estado,
    historial
):

    if estado[pos] == "Pendiente":
        print("Ya tiene una solicitud pendiente.")

    else:

        print(f"Dias disponibles: {dias_vacaciones[pos]}")

        try:
            dias = int(
                input("Cantidad de dias a solicitar (0 = Cancelar): ")
            )

            if dias == 0:
                print("Solicitud cancelada.")

            elif dias > 0 and dias <= dias_vacaciones[pos]:

                dias_solicitados[pos] = dias
                estado[pos] = "Pendiente"
                historial[pos] = "Solicitud de vacaciones enviada"

                print("Solicitud enviada a Recursos Humanos.")

            else:
                print("Cantidad de dias no valida.")

        except ValueError:
            print("Ingrese una cantidad valida.")


# ==========================================================
# MENU EMPLEADO
# ==========================================================

def menu_empleado(
    pos,
    nombres,
    ids,
    antiguedad,
    dias_vacaciones,
    dias_solicitados,
    salario_mensual,
    estado,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    while True:

        print("\n" + "=" * 45)
        print("            MENU EMPLEADO")
        print("=" * 45)

        print(f"Bienvenido: {nombres[pos]}")
        print("1. Solicitar vacaciones")
        print("2. Ver vacaciones")
        print("3. Ver salario mensual")
        print("4. Ver informacion")
        print("5. Ver ultimo movimiento")
        print("6. Ver recibo de pago")
        print("7. Cerrar sesion")

        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Opcion incorrecta.")
            continue

        if opcion == 1:

            vacaciones(
                pos, dias_vacaciones, dias_solicitados,
                estado, historial
            )

        elif opcion == 2:

            print(f"Estado: {estado[pos]}")
            print(f"Dias disponibles: {dias_vacaciones[pos]}")
            print(f"Dias solicitados: {dias_solicitados[pos]}")

        elif opcion == 3:

            print("Modalidad de pago: MENSUAL")
            print(f"Salario mensual: L. {salario_mensual[pos]:,.2f}")

        elif opcion == 4:

            print(f"ID: {ids[pos]}")
            print(f"Nombre: {nombres[pos]}")
            print(f"Antiguedad: {antiguedad[pos]} anos")
            print("Modalidad: MENSUAL")
            print(f"Salario mensual: L. {salario_mensual[pos]:,.2f}")

        elif opcion == 5:

            print(f"Ultimo movimiento: {historial[pos]}")

        elif opcion == 6:

            mostrar_recibo(
                pos, ids, nombres, salario_mensual,
                horas_extra, pago_horas_extra, rap,
                salario_anual, deducible_anual, excedente_anual,
                isr_anual, isr_mensual, deducciones,
                salario_bruto, salario_neto, pago_registrado
            )

        elif opcion == 7:

            print("Cerrando sesion...")
            break

        else:
            print("Opcion incorrecta.")

        input("\nPresione ENTER para continuar...")


# ==========================================================
# AGREGAR EMPLEADO
# ==========================================================

def agregar_empleado(
    cantidad,
    rol_sesion,
    ids,
    nombres,
    roles,
    antiguedad,
    dias_vacaciones,
    dias_solicitados,
    salario_mensual,
    estado,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    if cantidad >= 100:
        print("No se pueden agregar mas empleados. Limite alcanzado.")
        return cantidad

    try:
        nuevo_id = int(input("Ingrese nuevo ID (0 = Cancelar): "))
    except ValueError:
        print("ID invalido.")
        return cantidad

    if nuevo_id == 0:
        print("Registro cancelado.")
        return cantidad

    pos = buscar_empleado(cantidad, ids, nuevo_id)

    if pos != -1:
        print("Ese ID ya existe. El ID debe ser unico.")
        return cantidad

    cantidad += 1

    ids.append(nuevo_id)

    while True:

        nombre = input("Ingrese nombre: ").strip()

        if nombre == "":
            print("El nombre no puede estar vacio.")

        elif any(caracter.isdigit() for caracter in nombre):
            print("El nombre no puede contener numeros.")

        else:
            break

    nombres.append(nombre)

    while True:

        try:
            anios = int(input("Ingrese antiguedad en anos: "))

            if anios < 0:
                print("La antiguedad no puede ser negativa.")
            else:
                break

        except ValueError:
            print("Ingrese un numero entero valido.")

    antiguedad.append(anios)

    while True:

        try:
            salario = float(input("Ingrese salario MENSUAL: "))

            if salario < 0:
                print("El salario no puede ser negativo.")
            else:
                break

        except ValueError:
            print("Ingrese un salario valido.")

    salario_mensual.append(salario)

    dias = calcular_dias_vacaciones(anios)
    dias_vacaciones.append(dias)

    if rol_sesion == "ADMIN":

        print("Seleccione rol:")
        print("1. EMPLEADO")
        print("2. RRHH")

        try:
            opcion_rol = int(input("Seleccione: "))
        except ValueError:
            opcion_rol = 1

        if opcion_rol == 2:
            roles.append("RRHH")
        else:
            roles.append("EMPLEADO")

    else:
        roles.append("EMPLEADO")

    dias_solicitados.append(0)
    estado.append("Sin solicitud")
    historial.append("Empleado registrado")
    horas_extra.append(0)
    pago_horas_extra.append(0)

    rap.append(0)
    salario_anual.append(0)
    deducible_anual.append(DEDUCIBLE_ANUAL)
    excedente_anual.append(0)
    isr_anual.append(0)
    isr_mensual.append(0)
    deducciones.append(0)

    salario_bruto.append(salario)
    salario_neto.append(salario)
    pago_registrado.append(False)

    print("Empleado agregado correctamente.")

    return cantidad


# ==========================================================
# MODIFICAR EMPLEADO
# ==========================================================

def modificar_empleado(
    cantidad,
    ids,
    nombres,
    antiguedad,
    dias_vacaciones,
    salario_mensual,
    historial,
    pago_registrado
):

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Modificacion cancelada.")
        return

    while True:

        nombre = input("Nuevo nombre: ").strip()

        if nombre == "":
            print("El nombre no puede estar vacio.")

        elif any(caracter.isdigit() for caracter in nombre):
            print("El nombre no puede contener numeros.")

        else:
            break

    nombres[pos] = nombre

    while True:

        try:
            nuevos_anios = int(input("Nueva antiguedad: "))

            if nuevos_anios < 0:
                print("La antiguedad no puede ser negativa.")
            else:
                break

        except ValueError:
            print("Ingrese un numero valido.")

    antiguedad[pos] = nuevos_anios

    while True:

        try:
            nuevo_salario = float(input("Nuevo salario MENSUAL: "))

            if nuevo_salario < 0:
                print("El salario no puede ser negativo.")
            else:
                break

        except ValueError:
            print("Ingrese un salario valido.")

    salario_mensual[pos] = nuevo_salario

    dias_vacaciones[pos] = calcular_dias_vacaciones(nuevos_anios)

    pago_registrado[pos] = False
    historial[pos] = "Datos modificados"

    print("Empleado modificado.")


# ==========================================================
# ELIMINAR EMPLEADO
# ==========================================================

def eliminar_empleado(
    cantidad,
    id_sesion,
    ids,
    nombres,
    roles,
    antiguedad,
    dias_vacaciones,
    dias_solicitados,
    salario_mensual,
    estado,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Eliminacion cancelada.")
        return cantidad

    if ids[pos] == id_sesion:
        print("No puede eliminar su propia cuenta durante la sesion.")
        return cantidad

    listas = [
        ids, nombres, roles, antiguedad, dias_vacaciones,
        dias_solicitados, salario_mensual, estado, historial,
        horas_extra, pago_horas_extra, rap, salario_anual,
        deducible_anual, excedente_anual, isr_anual, isr_mensual,
        deducciones, salario_bruto, salario_neto, pago_registrado
    ]

    for lista in listas:
        lista.pop(pos)

    cantidad -= 1

    print("Empleado eliminado.")

    return cantidad


# ==========================================================
# REPORTE GENERAL
# ==========================================================

def reportes(
    cantidad,
    ids,
    nombres,
    roles,
    antiguedad,
    salario_mensual,
    dias_vacaciones,
    dias_solicitados,
    estado
):

    print("\n========== REPORTE DE EMPLEADOS ==========")

    for i in range(cantidad):

        print("-" * 40)
        print(f"ID: {ids[i]}")
        print(f"Nombre: {nombres[i]}")
        print(f"Rol: {roles[i]}")
        print(f"Antiguedad: {antiguedad[i]} anos")
        print("Modalidad: MENSUAL")
        print(f"Salario mensual: L. {salario_mensual[i]:,.2f}")
        print(f"Vacaciones disponibles: {dias_vacaciones[i]}")
        print(f"Dias solicitados: {dias_solicitados[i]}")
        print(f"Estado: {estado[i]}")


# ==========================================================
# REVISAR ULTIMO MOVIMIENTO
# ==========================================================

def revisar_historial(cantidad, ids, nombres, historial):

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Consulta cancelada.")
    else:
        print(f"Ultimo movimiento de {nombres[pos]}:")
        print(historial[pos])


# ==========================================================
# APROBAR / RECHAZAR VACACIONES
# ==========================================================

def revisar_solicitudes_vacaciones(
    cantidad,
    ids,
    nombres,
    dias_vacaciones,
    dias_solicitados,
    estado,
    historial
):

    print("\n========================================")
    print("       SOLICITUDES PENDIENTES")
    print("========================================")

    encontrado = False

    for i in range(cantidad):

        if estado[i] == "Pendiente":

            encontrado = True

            print(
                f"ID: {ids[i]} | "
                f"{nombres[i]} | "
                f"Dias: {dias_solicitados[i]}"
            )

    if not encontrado:
        print("No hay solicitudes pendientes.")
        return

    print("-" * 40)

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Revision cancelada.")
        return

    if estado[pos] != "Pendiente":

        print(
            "El empleado seleccionado no tiene "
            "solicitud pendiente."
        )
        return

    print(f"Empleado: {nombres[pos]}")
    print(f"Dias disponibles: {dias_vacaciones[pos]}")
    print(f"Dias solicitados: {dias_solicitados[pos]}")

    print("1. Aprobar")
    print("2. Rechazar")
    print("3. Mantener pendiente")
    print("0. Cancelar")

    try:
        opcion = int(input("Seleccione: "))
    except ValueError:
        print("Opcion incorrecta.")
        return

    if opcion == 1:

        estado[pos] = "Aprobada"
        dias_vacaciones[pos] -= dias_solicitados[pos]
        dias_solicitados[pos] = 0
        historial[pos] = "Vacaciones aprobadas por RRHH"

        print("Solicitud aprobada.")

    elif opcion == 2:

        estado[pos] = "Rechazada"
        dias_solicitados[pos] = 0
        historial[pos] = "Vacaciones rechazadas por RRHH"

        print("Solicitud rechazada.")

    elif opcion == 3:
        print("Solicitud permanece pendiente.")

    elif opcion == 0:
        print("Accion cancelada.")

    else:
        print("Opcion incorrecta.")


# ==========================================================
# PROCESAR / ACTUALIZAR PAGO MENSUAL
# ==========================================================

def procesar_pago_mensual(
    cantidad,
    ids,
    nombres,
    salario_mensual,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Calculo de planilla cancelado.")
        return

    print(f"Empleado: {nombres[pos]}")
    print(f"Salario mensual: L. {salario_mensual[pos]:,.2f}")

    try:
        nuevas_horas_extra = float(
            input(
                "Ingrese horas extra DIURNAS "
                "trabajadas este mes: "
            )
        )
    except ValueError:
        print("Ingrese un numero valido.")
        return

    if nuevas_horas_extra < 0:
        print("Las horas extra no pueden ser negativas.")
        return

    horas_extra[pos] = nuevas_horas_extra

    tasa_utilizada = calcular_pago_mensual(
        pos,
        salario_mensual,
        horas_extra,
        pago_horas_extra,
        rap,
        salario_anual,
        deducible_anual,
        excedente_anual,
        isr_anual,
        isr_mensual,
        deducciones,
        salario_bruto,
        salario_neto,
        pago_registrado
    )

    historial[pos] = "Planilla mensual calculada"

    print("\nPLANILLA CALCULADA CORRECTAMENTE")
    print("-" * 45)

    print(f"Pago por horas extra: L. {pago_horas_extra[pos]:,.2f}")
    print(f"Salario bruto: L. {salario_bruto[pos]:,.2f}")
    print(f"RAP (1.5%): L. {rap[pos]:,.2f}")

    print(f"Salario anual: L. {salario_anual[pos]:,.2f}")
    print(f"Deducible anual: L. {deducible_anual[pos]:,.2f}")
    print(f"Excedente anual: L. {excedente_anual[pos]:,.2f}")

    if tasa_utilizada == 0:
        print("Tasa ISR: EXENTO")
    else:
        print(f"Tasa ISR utilizada: {tasa_utilizada * 100:.0f}%")

    print(f"ISR anual: L. {isr_anual[pos]:,.2f}")
    print(f"ISR mensual: L. {isr_mensual[pos]:,.2f}")
    print(f"TOTAL DEDUCCIONES: L. {deducciones[pos]:,.2f}")
    print(f"SALARIO NETO: L. {salario_neto[pos]:,.2f}")


# ==========================================================
# VER PAGO DE EMPLEADO
# ==========================================================

def ver_pago(
    cantidad,
    ids,
    nombres,
    salario_mensual,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    pos = seleccionar_empleado(cantidad, ids)

    if pos == 0:
        print("Consulta cancelada.")
    else:

        mostrar_recibo(
            pos,
            ids,
            nombres,
            salario_mensual,
            horas_extra,
            pago_horas_extra,
            rap,
            salario_anual,
            deducible_anual,
            excedente_anual,
            isr_anual,
            isr_mensual,
            deducciones,
            salario_bruto,
            salario_neto,
            pago_registrado
        )


# ==========================================================
# REPORTE DE PLANILLA MENSUAL
# ==========================================================

def reporte_planilla(
    cantidad,
    ids,
    nombres,
    salario_mensual,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    print("\n========================================")
    print("      REPORTE DE PLANILLA MENSUAL")
    print("========================================")

    total_bruto = 0
    total_deducciones = 0
    total_neto = 0

    for i in range(cantidad):

        print("-" * 45)

        print(f"ID: {ids[i]}")
        print(f"Empleado: {nombres[i]}")
        print(f"Salario mensual: L. {salario_mensual[i]:,.2f}")

        if pago_registrado[i]:

            print(f"Horas extra: {horas_extra[i]:,.2f}")
            print(f"Pago horas extra: L. {pago_horas_extra[i]:,.2f}")
            print(f"Salario bruto: L. {salario_bruto[i]:,.2f}")
            print(f"RAP: L. {rap[i]:,.2f}")
            print(f"ISR mensual: L. {isr_mensual[i]:,.2f}")
            print(f"Deducciones: L. {deducciones[i]:,.2f}")
            print(f"Salario neto: L. {salario_neto[i]:,.2f}")

            total_bruto += salario_bruto[i]
            total_deducciones += deducciones[i]
            total_neto += salario_neto[i]

        else:
            print("Estado planilla: PENDIENTE DE CALCULAR")

    print("\n========================================")
    print("             TOTALES DE PLANILLA")
    print("========================================")
    print(f"Total salario bruto: L. {total_bruto:,.2f}")
    print(f"Total deducciones: L. {total_deducciones:,.2f}")
    print(f"TOTAL A PAGAR: L. {total_neto:,.2f}")


# ==========================================================
# RESUMEN DE COSTOS DE RRHH
# ==========================================================

def resumen_rrhh(
    cantidad,
    nombres,
    salario_bruto,
    deducciones,
    salario_neto,
    pago_registrado
):

    total_bruto = 0
    total_deducciones = 0
    total_neto = 0
    procesados = 0

    for i in range(cantidad):

        if pago_registrado[i]:

            total_bruto += salario_bruto[i]
            total_deducciones += deducciones[i]
            total_neto += salario_neto[i]
            procesados += 1

    print("\n========================================")
    print("        RESUMEN DE COSTOS DE RRHH")
    print("========================================")
    print(f"Empleados procesados: {procesados}")
    print(f"Empleados pendientes: {cantidad - procesados}")
    print(f"Total bruto: L. {total_bruto:,.2f}")
    print(f"Total deducciones: L. {total_deducciones:,.2f}")
    print(f"Total neto a pagar: L. {total_neto:,.2f}")


# ==========================================================
# MENU PLANILLA MENSUAL
# ==========================================================

def planilla(
    cantidad,
    ids,
    nombres,
    salario_mensual,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    while True:

        print("\n========================================")
        print("     PLANILLA - TRABAJADORES MENSUALES")
        print("========================================")

        print("1. Calcular / actualizar pago mensual")
        print("2. Ver recibo de empleado")
        print("3. Reporte de planilla")
        print("4. Resumen de costos de RRHH")
        print("5. Regresar al menu de RRHH")

        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Opcion incorrecta.")
            continue

        if opcion == 1:

            procesar_pago_mensual(
                cantidad, ids, nombres, salario_mensual,
                historial, horas_extra, pago_horas_extra,
                rap, salario_anual, deducible_anual,
                excedente_anual, isr_anual, isr_mensual,
                deducciones, salario_bruto, salario_neto,
                pago_registrado
            )

        elif opcion == 2:

            ver_pago(
                cantidad, ids, nombres, salario_mensual,
                horas_extra, pago_horas_extra, rap,
                salario_anual, deducible_anual, excedente_anual,
                isr_anual, isr_mensual, deducciones,
                salario_bruto, salario_neto, pago_registrado
            )

        elif opcion == 3:

            reporte_planilla(
                cantidad, ids, nombres, salario_mensual,
                horas_extra, pago_horas_extra, rap,
                salario_anual, deducible_anual, excedente_anual,
                isr_anual, isr_mensual, deducciones,
                salario_bruto, salario_neto, pago_registrado
            )

        elif opcion == 4:

            resumen_rrhh(
                cantidad, nombres, salario_bruto,
                deducciones, salario_neto, pago_registrado
            )

        elif opcion == 5:

            print("Regresando al menu de RRHH...")
            break

        else:
            print("Opcion incorrecta.")

        input("\nPresione ENTER para continuar...")


# ==========================================================
# MENU RRHH / ADMIN
# ==========================================================

def menu_rrhh(
    cantidad,
    pos_sesion,
    ids,
    nombres,
    roles,
    antiguedad,
    dias_vacaciones,
    dias_solicitados,
    salario_mensual,
    estado,
    historial,
    horas_extra,
    pago_horas_extra,
    rap,
    salario_anual,
    deducible_anual,
    excedente_anual,
    isr_anual,
    isr_mensual,
    deducciones,
    salario_bruto,
    salario_neto,
    pago_registrado
):

    id_sesion = ids[pos_sesion]
    rol_sesion = roles[pos_sesion]

    while True:

        print("\n========================================")
        print("         MENU RECURSOS HUMANOS")
        print("========================================")

        print(
            f"Usuario: {nombres[pos_sesion]} | "
            f"Rol: {rol_sesion}"
        )

        print("1. Agregar empleado")
        print("2. Modificar empleado")
        print("3. Eliminar empleado")
        print("4. Reporte de empleados")
        print("5. Revisar ultimo movimiento")
        print("6. Aprobar o rechazar vacaciones")
        print("7. Gestionar planilla mensual")
        print("8. Cerrar sesion")

        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Opcion incorrecta.")
            continue

        if opcion == 1:

            cantidad = agregar_empleado(
                cantidad, rol_sesion, ids, nombres, roles,
                antiguedad, dias_vacaciones, dias_solicitados,
                salario_mensual, estado, historial,
                horas_extra, pago_horas_extra, rap,
                salario_anual, deducible_anual, excedente_anual,
                isr_anual, isr_mensual, deducciones,
                salario_bruto, salario_neto, pago_registrado
            )

        elif opcion == 2:

            modificar_empleado(
                cantidad, ids, nombres, antiguedad,
                dias_vacaciones, salario_mensual,
                historial, pago_registrado
            )

        elif opcion == 3:

            cantidad = eliminar_empleado(
                cantidad, id_sesion, ids, nombres, roles,
                antiguedad, dias_vacaciones, dias_solicitados,
                salario_mensual, estado, historial,
                horas_extra, pago_horas_extra, rap,
                salario_anual, deducible_anual, excedente_anual,
                isr_anual, isr_mensual, deducciones,
                salario_bruto, salario_neto, pago_registrado
            )

        elif opcion == 4:

            reportes(
                cantidad, ids, nombres, roles, antiguedad,
                salario_mensual, dias_vacaciones,
                dias_solicitados, estado
            )

        elif opcion == 5:

            revisar_historial(
                cantidad, ids, nombres, historial
            )

        elif opcion == 6:

            revisar_solicitudes_vacaciones(
                cantidad, ids, nombres, dias_vacaciones,
                dias_solicitados, estado, historial
            )

        elif opcion == 7:

            planilla(
                cantidad, ids, nombres, salario_mensual,
                historial, horas_extra, pago_horas_extra,
                rap, salario_anual, deducible_anual,
                excedente_anual, isr_anual, isr_mensual,
                deducciones, salario_bruto, salario_neto,
                pago_registrado
            )

        elif opcion == 8:

            print("Cerrando sesion...")
            break

        else:
            print("Opcion incorrecta.")

        input("\nPresione ENTER para continuar...")


# ==========================================================
# ALGORITMO PRINCIPAL
# ==========================================================

def main():

    (
        ids, nombres, roles, antiguedad, dias_vacaciones,
        dias_solicitados, salario_mensual, estado, historial,
        horas_extra, pago_horas_extra, rap, salario_anual,
        deducible_anual, excedente_anual, isr_anual,
        isr_mensual, deducciones, salario_bruto, salario_neto,
        pago_registrado
    ) = inicializar_datos()

    cantidad = len(ids)

    cerrar_programa = False

    while not cerrar_programa:

        print("\n========================================")
        print("       SISTEMA DE GESTION RRHH")
        print("========================================")

        print("Ingrese su ID")
        print("0. Cerrar programa")

        try:
            id_usuario = int(input("ID: "))
        except ValueError:
            print("ID incorrecto.")
            continue

        if id_usuario == 0:

            cerrar_programa = True

        else:

            pos = buscar_empleado(
                cantidad,
                ids,
                id_usuario
            )

            if pos != -1:

                if roles[pos] == "EMPLEADO":

                    menu_empleado(
                        pos, nombres, ids, antiguedad,
                        dias_vacaciones, dias_solicitados,
                        salario_mensual, estado, historial,
                        horas_extra, pago_horas_extra, rap,
                        salario_anual, deducible_anual,
                        excedente_anual, isr_anual, isr_mensual,
                        deducciones, salario_bruto, salario_neto,
                        pago_registrado
                    )

                elif roles[pos] == "RRHH" or roles[pos] == "ADMIN":

                    menu_rrhh(
                        cantidad, pos, ids, nombres, roles,
                        antiguedad, dias_vacaciones,
                        dias_solicitados, salario_mensual,
                        estado, historial, horas_extra,
                        pago_horas_extra, rap, salario_anual,
                        deducible_anual, excedente_anual,
                        isr_anual, isr_mensual, deducciones,
                        salario_bruto, salario_neto,
                        pago_registrado
                    )

                else:
                    print("Usuario no autorizado.")

            else:
                print("ID incorrecto.")

    print("\nPrograma finalizado.")


# ==========================================================
# EJECUTAR PROGRAMA
# ==========================================================

if __name__ == "__main__":
    main()
