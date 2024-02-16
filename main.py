import flet as ft
import requests


#ENTER API TOKEN FROM https://home.openweathermap.org/api_keys !!!
weathertoken = ''

async def main(page: ft.Page):
    page.title = 'Погода'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    citytextfield = ft.TextField(label='Введите город', width=400)
    temperaturetxt = ft.Text()
    citytxt = ft.Text()
    

    async def closeerror(e):
        error_modal.open = False
        await page.update_async()

    
    error_modal = ft.AlertDialog(
        modal=True,
        title=ft.Icon(ft.icons.ERROR),
        content=ft.Text('Произошла ошибка получения погоды!'),
        actions=[
            ft.OutlinedButton('Закрыть', on_click=closeerror)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    

    async def change_theme(e):
        if page.theme_mode == 'dark':
            page.theme_mode = 'light'
        else:
            page.theme_mode = 'dark'
        await page.update_async()

    

    async def get_weather(e):
        try:
            if len(citytextfield.value) < 2:
                return

            url = f'https://api.openweathermap.org/data/2.5/weather?q={citytextfield.value}&appid={weathertoken}&units=metric'
            weatherdata = requests.get(url).json()
            temp = weatherdata['main']['temp']
            citytxt.value = f'🏙️ Город: {citytextfield.value}'
            temperaturetxt.value = f'☁️ Погода: {temp}℃'
            await page.update_async()
        
        except Exception:
            page.dialog = error_modal
            error_modal.open = True
            await page.update_async()

    await page.add_async(
        ft.Row(
            [
                ft.IconButton(ft.icons.LIGHT_MODE, on_click=change_theme),
                ft.Text('Погода')
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    await page.add_async(
        ft.Row(
            [
                citytextfield,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    await page.add_async(
        ft.Row(
            [
                ft.OutlinedButton(text='Посмотреть', on_click=get_weather)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    await page.add_async(
        ft.Row(
            [
                ft.Text()
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )
    await page.add_async(
        ft.Row(
            [
                citytxt
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )
    await page.add_async(
        ft.Row(
            [
                temperaturetxt
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )

ft.app(target=main)

