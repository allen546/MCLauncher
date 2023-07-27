from nicegui import ui
from ..core.launch import quickstart, LATEST_MINECRAFT_STABLE

@ui.page("/")
def index():
    with ui.header().classes(replace='row items-center') as header:
        ui.button(icon='style').props('flat color=white')
        with ui.tabs() as tabs:
            ui.tab('启动')
            ui.tab('下载')
            ui.tab('选项')

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

    with ui.tab_panels(tabs, value='启动').classes('w-full'):
        with ui.tab_panel('启动'):
            ui.button("启动最新版"+str(LATEST_MINECRAFT_STABLE), on_click=quickstart)
            ui.label('LauncherNext').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        with ui.tab_panel('下载'):
            ui.label('Content of B')
        with ui.tab_panel('选项'):
            dark = ui.dark_mode()
            ui.label('切换主题:')
            ui.button('暗色', on_click=dark.enable)
            ui.button('亮色', on_click=dark.disable)
            ui.label('切换色调:')
            ui.button('默认蓝', on_click=lambda: ui.colors())
            ui.button('低调灰', on_click=lambda: ui.colors(primary='#555'))
            #dummy switches
            switch1 = ui.switch('switch me')
            switch2 = ui.switch('switch me')
            switch3 = ui.switch('switch me')
            switch4 = ui.switch('switch me')
            switch5 = ui.switch('switch me')
            switch6 = ui.switch('switch me')

