import flet as ft
import os

def main(page: ft.Page):
    page.title = "SISTEMA EDEN"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    archivo_notas = "mis_notas_grafica.txt"
    archivo_users = "usuarios.txt"

    # --- FUNCIONES ---
    def ir_a_registro(e):
        vista_login.visible = False
        vista_eden.visible = True
        page.update()

    def ejecutar_registro(e):
        u = user_reg.value.strip()
        p = pass_reg.value.strip()
        if u != "" and p != "":
            with open(archivo_users, "a") as f:
                f.write(f"{u}:{p}\n")
            page.snack_bar = ft.SnackBar(ft.Text("Usuario creado correctamente"), bgcolor="green")
            page.snack_bar.open = True
            vista_eden.visible = False
            vista_login.visible = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Incorrecto, intenta de nuevo"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    def validar_acceso(e):
        u = user_in.value.strip()
        p = pass_in.value.strip()
        encontrado = False
        if os.path.exists(archivo_users):
            with open(archivo_users, "r") as f:
                for linea in f:
                    if ":" in linea:
                        u_db, p_db = linea.strip().split(":")
                        if u == u_db and p == p_db:
                            encontrado = True
                            break
        
        if encontrado or (u == "admin" and p == "1234"):
            vista_login.visible = False
            vista_agenda.visible = True
            cargar_notas()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Incorrecto, intenta de nuevo"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    def cerrar_sesion(e):
        vista_agenda.visible = False
        user_in.value = ""
        pass_in.value = ""
        vista_login.visible = True
        page.update()

    # --- VISTA 1: LOGIN ---
    user_in = ft.TextField(label="Usuario", width=300)
    pass_in = ft.TextField(label="Contraseña", password=True, width=300)
    
    vista_login = ft.Column([
        ft.Text("INICIO DE SESIÓN", size=25, weight="bold", color="blue"),
        user_in, pass_in,
        ft.ElevatedButton("ENTRAR", on_click=validar_acceso, bgcolor="blue", color="white", width=300),
        ft.TextButton("¿No tienes cuenta? REGÍSTRATE AQUÍ", on_click=ir_a_registro)
    ], horizontal_alignment="center", visible=True)

    # --- VISTA 2: BIENVENIDOS AL EDEN ---
    user_reg = ft.TextField(label="Nuevo Usuario", width=300)
    pass_reg = ft.TextField(label="Nueva Contraseña", password=True, width=300)
    
    vista_eden = ft.Column([
        ft.Text("BIENVENIDOS AL EDEN", size=40, weight="bold", color="cyan", italic=True),
        ft.Text("REGÍSTRATE", size=20, color="cyan"),
        user_reg, pass_reg,
        ft.ElevatedButton("CREAR CUENTA", on_click=ejecutar_registro, bgcolor="cyan", color="black", width=300),
        ft.TextButton("Volver al Login", on_click=lambda _: [setattr(vista_eden, 'visible', False), setattr(vista_login, 'visible', True), page.update()])
    ], visible=False, horizontal_alignment="center")

    # --- VISTA 3: AGENDA ---
    lista_tareas = ft.Column(scroll="auto", height=350)
    campo_tarea = ft.TextField(label="Nueva tarea...", expand=True)

    def cargar_notas():
        lista_tareas.controls.clear()
        if os.path.exists(archivo_notas):
            with open(archivo_notas, "r") as f:
                for linea in f:
                    if linea.strip():
                        lista_tareas.controls.append(ft.Checkbox(label=linea.strip()))
        page.update()

    def guardar_tarea(e):
        if campo_tarea.value.strip():
            with open(archivo_notas, "a") as f:
                f.write(campo_tarea.value + "\n")
            campo_tarea.value = ""
            cargar_notas()

    def borrar_marcados(e):
        restantes = [c.label for c in lista_tareas.controls if not c.value]
        with open(archivo_notas, "w") as f:
            for r in restantes: f.write(r + "\n")
        cargar_notas()

    vista_agenda = ft.Column([
        ft.Row([
            ft.Text("MIS TAREAS", size=30, weight="bold", color="blue"),
            ft.ElevatedButton("SALIR", on_click=cerrar_sesion, bgcolor="red", color="white")
        ], alignment="spaceBetween"),
        ft.Row([campo_tarea, ft.ElevatedButton("AÑADIR", on_click=guardar_tarea, bgcolor="blue", color="white")]),
        ft.ElevatedButton("BORRAR MARCADOS", on_click=borrar_marcados, bgcolor="orange", color="white", width=400),
        ft.Divider(),
        lista_tareas,
    ], visible=False)

    page.add(vista_login, vista_eden, vista_agenda)
ft.app(target=main)
