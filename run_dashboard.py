# run_dashboard.py
import subprocess
import sys
import os
import webbrowser
import time

def get_path(filename_in_bundle):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename_in_bundle)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename_in_bundle)

if __name__ == "__main__":
    dashboard_script_name = "dashboard_arsat.py"
    dashboard_script_path = get_path(dashboard_script_name)

    print(f"Lanzando dashboard desde: {dashboard_script_path}")
    if not os.path.exists(dashboard_script_path):
        print(f"Error: No se encontró el script del dashboard en {dashboard_script_path}")
        input("Presiona Enter para salir.")
        sys.exit(1)

    # Intentar construir la ruta al python.exe del entorno virtual o del sistema
    # Esto es crucial para evitar que el .exe se llame a sí mismo.
    if hasattr(sys, "_MEIPASS"):
        # En un entorno congelado, necesitamos una forma de llamar a un python.exe "real"
        # PyInstaller debería haber empaquetado uno. Intentar encontrarlo.
        # Esta ruta puede variar dependiendo de la estructura de PyInstaller.
        # A menudo, el python.exe está en la misma carpeta que el .exe principal en el modo de un directorio,
        # o en una subcarpeta.
        # Si estamos en modo --onefile, _MEIPASS es una carpeta temporal.
        # Vamos a asumir que PyInstaller hace que "python.exe" (o "python") esté disponible
        # en el PATH temporal del entorno del .exe, o que un python del sistema es accesible.
        # La forma más simple y a menudo efectiva es simplemente llamar a "python".
        python_executable_for_streamlit = "python"
    else:
        # En desarrollo, sys.executable es el python.exe correcto.
        python_executable_for_streamlit = sys.executable
        
    cmd = [
        python_executable_for_streamlit, # Usar el python determinado
        "-m", 
        "streamlit", 
        "run", 
        dashboard_script_path, 
        "--server.headless", "true", 
        "--server.port", "8501",     
        "--server.fileWatcherType", "none" 
    ]

    print(f"Ejecutando comando: {' '.join(cmd)}")
    
    try:
        startupinfo = None
        if os.name == 'nt': 
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # startupinfo.wShowWindow = subprocess.SW_HIDE # Descomentar para intentar ocultar la consola de Streamlit

        # Usar Popen para no bloquear y permitir que el lanzador continúe/termine
        process = subprocess.Popen(cmd, startupinfo=startupinfo)
        
        print("Esperando a que el servidor de Streamlit inicie (aprox. 8 segundos)...")
        time.sleep(8) 
        
        # Verificar si el proceso sigue corriendo (una verificación simple)
        if process.poll() is None: # None significa que sigue corriendo
            print("Abriendo el dashboard en el navegador...")
            webbrowser.open("http://localhost:8501")
            print("\nEl dashboard debería estar corriendo en tu navegador en http://localhost:8501")
            print("Esta ventana del lanzador se puede cerrar. Para detener el dashboard, cierra la pestaña del navegador")
            print("y, si es necesario, el proceso 'streamlit' o 'python' desde el Administrador de Tareas.")
        else:
            print("Error: El proceso de Streamlit terminó inesperadamente.")
            print(f"Código de salida del proceso: {process.poll()}")
            stdout, stderr = process.communicate()
            if stdout: print(f"Salida del proceso: {stdout.decode(errors='ignore')}")
            if stderr: print(f"Errores del proceso: {stderr.decode(errors='ignore')}")
            input("Presiona Enter para salir.")

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el comando '{python_executable_for_streamlit}' o el módulo 'streamlit'.")
        input("Presiona Enter para salir.")
    except Exception as e:
        print(f"Ocurrió un error al lanzar el dashboard: {e}")
        input("Presiona Enter para salir.")