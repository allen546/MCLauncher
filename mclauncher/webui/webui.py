
# EDIT ON 07/28/23

from functools import partial
import threading
import time
import os
import subprocess
import zipfile
import json
from nicegui import ui
from ..core.launch import quickstart, LATEST_MINECRAFT_STABLE
from ..core.versions import VersionDecoder, VersionDecoder2
from ..core.utils import *

cwd = os.getcwd()
__version__ = '0.2' 

# os.system('mkdir lnxt')

try:
    with open("versions.json", "r") as f:
        versions = json.loads(f.read(), object_hook=VersionDecoder2)
        f.seek(0)
        version2 = json.loads(f.read(), object_hook=VersionDecoder)
        version_dict = dict(zip(versions, version2))
        # print(version_dict)
        print('[INFO] Config loaded.')
except FileNotFoundError:
    print('[WARN] Config file not detected.')


def mc_loop(realversion, footer, launch_bt, start2, logs):
    def real():
        process = quickstart(minecraft_version=realversion)
        while True:
            # time.sleep(1)
            if process.poll() is not None:
                break
            ln = process.stdout.readline()
            print(ln.decode(), end="")
            logs.push(ln.decode().strip())
            if ln.decode().strip().endswith("Stopping!"):
                break
        n = process.stdout.read().decode()
        print(n)
        logs.push(n)
        footer.hide()
        logs.clear()
        launch_bt.visible = True
        start2.enable()

    return real


@ui.page('/')
def launch():
    def launch_mc(version_getter):
        footer.show()
        launch_bt.visible = False
        start = ButtonGroup()
        start.add_button(start2)
        start.add_button(start1)
        start.disable()
        # ver_name = f'"{version}"'

        #version = ver_select.value
        version = version_getter()
        realversion = version_dict[version]
        print("[INFO] Starting Minecraft", version)
        logs.push("[INFO] Starting Minecraft "+version)
        # time.sleep(10)
        threading.Thread(target=mc_loop(realversion, footer, launch_bt, start, logs)).start()

    def launch_mc_now():
        footer.show()
        launch_bt.visible = False
        start = ButtonGroup()
        start.add_button(start2)
        start.add_button(start1)
        start.disable()
        # ver_name = f'"{version}"'

        version = ver_select.value
        realversion = version_dict[version]
        print("[INFO] Starting Minecraft", version)
        # time.sleep(10)
        threading.Thread(target=mc_loop(realversion, footer, launch_bt, start, logs)).start()

    def get_launch_mc(bind_to):
        def getter():
            return bind_to.value
        def callback():
            return launch_mc(getter)
        return callback

    with ui.dialog() as dialog, ui.card():
        with ui.column():
            ui.label('关于 LauncherNext').style(
                'color: #6E93D6; font-size: 200%; font-weight: 300'
            )
            ui.label('LauncherNext v' + __version__)
            ui.label('一个由Allen546和DarkstarXD共同开发的webUI轻量级Minecraft启动器。')
            ui.button('关闭', on_click=dialog.close)

    with ui.header().classes(replace='row items-center') as header:
        ui.button(icon='launch', on_click=dialog.open).props('flat color=white').tooltip(
            'LauncherNext v' + __version__
        )
        with ui.tabs() as tabs:
            ui.tab('启动')
            ui.tab('版本')
            ui.tab('下载')
            ui.tab('Mod管理')
            ui.tab('选项')

    with ui.footer(value=False).style("height:20%") as footer:
        ui.label('正在启动Minecraft').style('color: #FFFFFF; font-size: 200%; font-weight: 300')
        with ui.column().style("width: 100%; height: 100%"):
            # To use the progressbar(which is developing) with no actual use:
            logs = ui.log().style("width: 100%; height: 70%;background-color: #000000; text-color: #FFFFFF")
            #progressbar = ui.linear_progress(value=0).props('instant-feedback').style("width:100%;")

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        launch_bt = ui.button(on_click=launch_mc_now, icon='rocket').props('fab')
        

    with ui.tab_panels(tabs, value='启动').classes('w-full'):
        with ui.tab_panel('启动'):
            ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.label('\u00a0')  # Added some spaces through the interface
            ui.separator()
            ui.label('\u00a0')
            with ui.row().style("width: 99%;"):
                with ui.card().style("width: 49%; height: 100%"):
                    with ui.column():
                        ui.label('简易启动')
                        ver_select2 = ui.select(versions, value=str(versions[0]))
                        start1 = ui.button("启动Minecraft", on_click=get_launch_mc(ver_select2))
                        # ui.button('管理登录', on_click=login).tooltip('管理Littleskin登录通行证')
                        checkbox = ui.checkbox('使用离线登录(用户名为Steve)')
                        # chk_var = ui.checkbox('补全文件 (会拖慢启动速度，但能解决大部分问题)')
                ui.label('\u00a0')
                with ui.card().style("width: 49%; height: 100%"):
                    with ui.column():
                        ui.label('自定义启动')
                        ver_select = ui.select(versions, value=str(versions[0]))
                        start2 = ui.button("启动Minecraft", on_click=get_launch_mc(ver_select))
                        # ui.button('管理登录', on_click=login).tooltip('管理Littleskin登录通行证')
                        checkbox = ui.checkbox('使用离线登录(用户名为Steve)')
                        # chk_var = ui.checkbox('补全文件 (会拖慢启动速度，但能解决大部分问题)')

        with ui.tab_panel('版本'):
            ui.label("Version")


        with ui.tab_panel('下载'):
            ui.label('Content of B')

        with ui.tab_panel('选项'):
            dark = ui.dark_mode()
            with ui.card():
                ui.label('UI个性化').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                ui.label('切换主题:')
                ui.button('暗色', on_click=dark.enable)
                ui.button('亮色', on_click=dark.disable)
                ui.separator()
                ui.label('切换色调:')
                ui.button('默认蓝', on_click=lambda: ui.colors())
                ui.button('低调灰', on_click=lambda: ui.colors(primary='#555'))
            ui.label('\u00a0')
            with ui.card():
                ui.label('Minecraft实例').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                with ui.column():
                    switch1 = ui.switch('启用版本隔离')
                    switch2 = ui.switch('强制使用指定Java')
                    switch3 = ui.switch('DUMMY SWITCH')
                    switch4 = ui.switch('switch me')
                    switch5 = ui.switch('switch me')
                    switch6 = ui.switch('switch me')
            ui.label('\u00a0')
            with ui.card():
                ui.label('启动选项').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                with ui.column():
                    switch1 = ui.switch('1')
                    switch2 = ui.switch('2')
                    switch3 = ui.switch('3')
                    switch4 = ui.switch('4')
                    switch5 = ui.switch('A')
                    switch6 = ui.switch('B')
