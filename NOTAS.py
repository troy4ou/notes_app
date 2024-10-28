import flet as ft
import os
import json
json_db = "database.json"  # Nombre del archivo JSON para almacenar las tareas.




input_task = ft.TextField(  # Campo de entrada para nuevas tareas




    label="NOTA:",
    label_style= ft.TextStyle(color=ft.colors.GREEN), 
    col=12,
    width=600,
    tooltip="Escribe tu nota",
    hover_color=ft.colors.WHITE24,
    focused_border_color=ft.colors.GREEN,
    focused_border_width=3,
    cursor_color= ft.colors.GREEN,
    autofocus = True,
    on_submit = lambda e: add_task(e,page = ft.Page),
    on_change = lambda e:change_color_input_button(e)
)  
input_button = ft.IconButton(
    tooltip="Añadir Nota",
    icon=ft.icons.TASK_ALT_OUTLINED,
    icon_size=30,
    on_click = lambda e: add_task(e,page = ft.Page)
)
button_delete_all = ft.IconButton(
                            icon = ft.icons.DELETE_SWEEP_ROUNDED,
                            icon_size = 30,
                            icon_color=ft.colors.RED_500,
                            tooltip = "Borrar Todo",
                            highlight_color = ft.colors.RED_100,
                            on_click=lambda e: delete_task(e,page = ft.Page),
)

def load_tasks():
    #Load the tasks from the JSON file if it exists.



    if os.path.exists(json_db):
        try:
            with open(json_db, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(data):
    #Save tasks to a JSON file.



    with open(json_db, "w") as file:
        json.dump(data, file, indent=2)

def add_task(e,page):
    #Add a new task to the task list.



    data = load_tasks()
    new_task = {"task": input_task.value.strip()}
    if new_task["task"]:  # Verificar que la tarea no esté vacía




        data.append(new_task)
        input_task.value = ""  # Borrar campo de entrada




        input_task.update()
        save_tasks(data)
        change_color_input_button(e)
        update_task_list(page)  # Actualice la lista de tareas en la interfaz.





def delete_task(e, page, task_text=None):
    #Delete a task from the task list.



    data = load_tasks()
    if task_text is not None:
        data = [task for task in data if task["task"] != task_text]
    elif e.control == button_delete_all:
        data = []
    save_tasks(data)
    update_task_list(page)
    

def update_task_list(page):
    #Update the task list displayed on the interface.



    data = load_tasks()
    data.reverse()
    task_list_container.controls.clear()  # Limpiar tareas existentes en la interfaz.




    for task in data:
        task_text = task["task"]
        task_row = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.DELETE_FOREVER_OUTLINED,
                    icon_size=25,
                    icon_color=ft.colors.RED,
                    hover_color=ft.colors.with_opacity(0.2,ft.colors.RED_500),
                    width=70,
                    tooltip="Borrar Nota",
                    on_click=lambda e, task_text=task_text: delete_task(e, page, task_text)
                ),
                ft.Text(task_text, text_align=ft.TextAlign.LEFT, size=18, expand=5,animate_size=20),
            ], spacing=20,
        )
        column_list = ft.Column(width=900)
        column_list.controls.append(task_row)
        task_list_container.controls.append(column_list)  # Agregar cola de tareas al contenedor




    task_list_container.update()

def change_color_input_button(e):
    if input_task.value.split():
        input_button.icon_color = ft.colors.GREEN
    else:
        input_button.icon_color = ft.colors.GREY
    input_button.update()

def main(page: ft.Page):
    page.window.icon = "./icon.png"
    page.title = "NOTAS"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 750
    page.window_min_height = 500
    page.window_center()
    input_task.value = ""  # Borrar campo de entrada al cargar la página 




    global task_list_container
    task_list_container =ft.ListView(expand=1,spacing=5,height=900,width=750,item_extent=200)  # Contenedor para la lista de tareas.




    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        input_task,
                        input_button,
                        button_delete_all,
                    ],alignment=ft.MainAxisAlignment.CENTER,
                ),ft.Column(
                    controls=[task_list_container],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height= 900,
                    scroll =ft.ScrollMode.ALWAYS,
                ),
                      # Muestra la lista de tareas




            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    # Inicializar la lista de tareas al cargar la página




    update_task_list(page)
ft.app(target=main,view=ft.AppView.FLET_APP_HIDDEN)