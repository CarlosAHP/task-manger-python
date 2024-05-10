import tkinter as tk
from tkinter import ttk, messagebox
import psutil

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.configure(background='#2E2E2E')

        self.establecer_estilo()

        # Configuración del Treeview para mostrar procesos
        self.tree = ttk.Treeview(root, columns=('PID', 'Nombre', 'Memoria'), show='headings')
        self.tree.heading('PID', text='PID', anchor='center')
        self.tree.heading('Nombre', text='Nombre', anchor='center')
        self.memoria_column_title = 'Memoria (MB)'
        self.tree.heading('Memoria', text=self.memoria_column_title, anchor='center')
        self.tree.column('PID', width=50, anchor='center')
        self.tree.column('Nombre', width=300, anchor='center')
        self.tree.column('Memoria', width=100, anchor='center')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.actualizar_procesos()

        # Entrada de búsqueda y botón
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.search_entry.bind("<Return>", lambda event: self.filtrar_procesos())  
        ttk.Button(root, text="Buscar", command=self.filtrar_procesos, style='White.TButton').pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Frame para botones de "Finalizar Tarea", "Actualizar Procesos" y "Seleccionar Proceso"
        frame_botones_procesos = tk.Frame(root, bg='#2E2E2E')
        frame_botones_procesos.pack(side=tk.TOP, fill=tk.X, padx=15, pady=(0, 15))

        # Botones con nuevo estilo y posición
        ttk.Button(frame_botones_procesos, text="Finalizar Tarea", command=self.finalizar_tarea, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones_procesos, text="Actualizar Procesos", command=self.actualizar_procesos, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones_procesos, text="Seleccionar Proceso", command=self.seleccionar_proceso, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)

        # Lista para procesos seleccionados, ahora abajo
        self.lista_seleccionados = tk.Listbox(root, width=50, height=20, bg='#4D4D4D', fg='white')
        self.lista_seleccionados.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

        # Frame para los botones
        frame_botones = tk.Frame(root, bg='#2E2E2E')
        frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

        # Botones con nuevo estilo y posición
        ttk.Button(frame_botones, text="Procesar FIFO", command=lambda: self.procesar_seleccionados('FIFO'), style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones, text="Procesar LIFO", command=lambda: self.procesar_seleccionados('LIFO'), style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones, text="FIFO vs LIFO", command=self.comparar_fifo_lifo, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones, text="Eliminar Proceso Seleccionado", command=self.eliminar_proceso_seleccionado, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_botones, text="Clear", command=self.limpiar_selecciones, style='White.TButton').pack(side=tk.LEFT, padx=5, pady=5)

        # Centrar los botones en el frame_botones
        for child in frame_botones.winfo_children():
            child.pack_configure(anchor='center')

    # Métodos restantes sin cambios

    def filtrar_procesos(self):
        filtro = self.search_var.get().lower()
        matches = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if filtro in values[1].lower():
                matches.append(item)

        if matches:
            self.tree.see(matches[0])
            self.tree.selection_set(matches[0])
        else:
            self.tree.selection_remove(self.tree.selection())

    def limpiar_selecciones(self):
        self.lista_seleccionados.delete(0, tk.END)

    def finalizar_tarea(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            proceso_info = self.tree.item(seleccionado, 'values')
            pid = proceso_info[0]
            try:
                pid = int(pid)
                proceso = psutil.Process(pid)
                proceso.terminate()
                messagebox.showinfo("Finalizar Tarea", f"El proceso {pid} ha sido finalizado.")
                self.actualizar_procesos()
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "El proceso no existe.")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "Acceso denegado para finalizar el proceso.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def ordenar_az(self):
        items = self.tree.get_children()
        items = sorted(items, key=lambda x: self.tree.item(x, 'values')[1].lower())  # Ordena por nombre (columna 2)
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert('', 'end', values=self.tree.item(item, 'values'))

    def ordenar_por_memoria(self):
        items = self.tree.get_children()
        items = sorted(items, key=lambda x: float(self.tree.item(x, 'values')[2].split()[0]))  # Ordena por memoria (columna 3)
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert('', 'end', values=self.tree.item(item, 'values'))

    def establecer_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('Treeview', background='#191919', foreground='white', fieldbackground='#2D2D2D')
        estilo.configure('Treeview.Heading', background='#2D2D2D', foreground='white')
        estilo.configure('TButton', foreground='black')
        estilo.map('TButton', background=[('active', '#4D4D4D')], foreground=[('active', 'white')])
        estilo.configure('White.TButton', background='white', foreground='black')

    # Los métodos restantes se mantienen igual



    def obtener_procesos(self):
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'username']):
            try:
                procesos.append({
                    'pid': proc.pid,
                    'nombre': proc.name(),
                    'memoria': proc.memory_info().rss / 1024 ** 2,
                    'usuario': proc.username()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return procesos

    def actualizar_procesos(self):
        # Calcular el porcentaje total de memoria utilizada
        total_memory = psutil.virtual_memory().total
        used_memory = psutil.virtual_memory().used
        memory_usage_percent = (used_memory / total_memory) * 100

        # Actualizar el título de la columna 'Memoria' para mostrar el porcentaje total de memoria utilizada
        self.tree.heading('Memoria', text=f'Memoria  {memory_usage_percent:.2f}%')

        self.tree.delete(*self.tree.get_children())
        for proceso in self.obtener_procesos():
            memoria_texto = f"{round(proceso['memoria'], 2)} MB"
            self.tree.insert('', tk.END, values=(proceso['pid'], proceso['nombre'], memoria_texto, proceso['usuario']))

        #self.root.after(2000, self.actualizar_procesos)    


    def seleccionar_proceso(self):
        for item in self.tree.selection():
            proceso = self.tree.item(item)['values']
            proceso_str = f"{proceso[1]} - PID: {proceso[0]} - Memoria: {proceso[2]}"
            if proceso_str not in self.lista_seleccionados.get(0, tk.END):
                self.lista_seleccionados.insert(tk.END, proceso_str)

    def eliminar_proceso_seleccionado(self):
        seleccionado = self.lista_seleccionados.curselection()
        if seleccionado:
            self.lista_seleccionados.delete(seleccionado)

    def procesar_seleccionados(self, metodo):
        def eliminar_primero():
            if self.lista_seleccionados.size() > 0:
                self.lista_seleccionados.delete(0)
                self.root.after(1000, eliminar_primero)  # 500 ms de espera antes de eliminar el siguiente

        def eliminar_ultimo():
            if self.lista_seleccionados.size() > 0:
                self.lista_seleccionados.delete(self.lista_seleccionados.size() - 1)
                self.root.after(1000, eliminar_ultimo)  # 500 ms de espera antes de eliminar el siguiente

        if metodo == 'FIFO':
            eliminar_primero()
        elif metodo == 'LIFO':
            eliminar_ultimo()

    def comparar_fifo_lifo(self):
        # Crear una nueva ventana
        ventana_comparacion = tk.Toplevel(self.root)
        ventana_comparacion.title("Comparación FIFO vs LIFO")

        # Marco para FIFO
        frame_fifo = tk.Frame(ventana_comparacion)
        frame_fifo.pack(side=tk.LEFT, padx=10, pady=10)
        label_fifo = tk.Label(frame_fifo, text="FIFO", bg='#4D4D4D', fg='white')
        label_fifo.pack()
        lista_fifo = tk.Listbox(frame_fifo, width=50, height=20, bg='#4D4D4D', fg='white')
        lista_fifo.pack()

        # Marco para LIFO
        frame_lifo = tk.Frame(ventana_comparacion)
        frame_lifo.pack(side=tk.RIGHT, padx=10, pady=10)
        label_lifo = tk.Label(frame_lifo, text="LIFO", bg='#4D4D4D', fg='white')
        label_lifo.pack()
        lista_lifo = tk.Listbox(frame_lifo, width=50, height=20, bg='#4D4D4D', fg='white')
        lista_lifo.pack()

        # Copia los elementos de la lista principal a FIFO y LIFO
        for proceso in self.lista_seleccionados.get(0, tk.END):
            lista_fifo.insert(tk.END, proceso)
            lista_lifo.insert(tk.END, proceso)

        def procesar_fifo():
            if lista_fifo.size() > 0:
                lista_fifo.delete(0)
                ventana_comparacion.after(2000, procesar_fifo)

        def procesar_lifo():
            if lista_lifo.size() > 0:
                lista_lifo.delete(lista_lifo.size() - 1)
                ventana_comparacion.after(2000, procesar_lifo)

        # Espera 2 segundos antes de comenzar la animación
        ventana_comparacion.after(2000, procesar_fifo)
        ventana_comparacion.after(2000, procesar_lifo)



if __name__ == '__main__':
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()


