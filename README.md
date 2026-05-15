#### **Iris Sucely Piló Guarcax**, 20250621  
Facultad de Ciencias Económicas  
Estructura de Datos y Algoritmos  
Catedrático: Luis Angel Tórtola  
Auxiliar: Christian Barrios  
PROYECTO FINAL - PRIORITY QUEUE  

---
# Pizzería — Sistema de Gestión de Órdenes con Priority Queue

Sistema web para gestionar la cola de órdenes de una pizzería, utilizando una **Priority Queue** implementada desde cero en Python.


---

## Descripción

Las órdenes no se procesan en orden de llegada, sino según su **prioridad**, determinada por:
- Tipo de orden: `express (30)` > `para_llevar (20)` > `mesa (10)`
- Tiempo de espera acumulado (se suma dinámicamente a la prioridad base)

Esto hace que la Priority Queue sea la estructura óptima: soporta inserciones y extracciones eficientes con prioridades que cambian en tiempo real.

---

## Estructura de datos: Max-Heap Priority Queue

Implementada en `priority_queue.py` completamente desde cero, sin librerías externas.

### Representación interna
El heap se representa como un **arreglo/lista de Python**. Para el nodo en índice `i`:
- Padre: `(i - 1) // 2`
- Hijo izquierdo: `2i + 1`
- Hijo derecho: `2i + 2`

### Métodos y complejidad temporal

| Método | Descripción | Complejidad |
|---|---|---|
| `insert(order)` | Inserta al final y aplica heapify_up | O(log n) |
| `extract_max()` | Extrae la raíz, reemplaza con el último y aplica heapify_down | O(log n) |
| `peek()` | Retorna la raíz sin extraerla | O(1) |
| `update_priority(id, p)` | Busca por ID y reordena hacia arriba o abajo | O(n) |
| `delete(id)` | Sube el nodo a la raíz con prioridad infinita y extrae | O(n) |
| `add_wait_time(min)` | Actualiza todos los nodos y reconstruye el heap | O(n log n) |
| `is_empty()` | Verifica si el heap está vacío | O(1) |
| `size()` | Retorna el número de elementos | O(1) |
| `get_all()` | Retorna todos los elementos ordenados | O(n log n) |

---

## Funcionalidades core

1. **Registrar nueva orden** — se inserta con prioridad calculada automáticamente según tipo.
2. **Procesar la orden más urgente** — extrae siempre la orden de mayor prioridad (extract_max).
3. **Consultar siguiente orden** — peek sin extraer, visible en la interfaz en todo momento.
4. **Actualizar prioridad** — modifica la prioridad de cualquier orden y reordena el heap.
5. **Cancelar orden** — elimina una orden de cualquier posición del heap.
6. **Visualizar la cola completa** — todas las órdenes ordenadas por prioridad de mayor a menor.

### Funcionalidad adicional:
7. **Simular tiempo de espera** — incrementa dinámicamente la prioridad de todas las órdenes activas según minutos de espera acumulados. 

---

## Instalación y ejecución local

### Requisitos
- Python 3.8+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone git@github.com:irispilo/FINAL-PROJECT-DSA.git
cd FINAL-PROJECT-DSA

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install flask

# 4. Ejecutar la aplicación
python app.py

# 5. Abrir en el navegador
# http://localhost:5000
```

### Ejecutar tests

```bash
pytest test_priority_queue.py -v
```
---

## Estructura del proyecto

```
FINAL-PROJECT-DSA/
├── app.py                  # Flask backend + rutas API
├── priority_queue.py       # Implementación Max-Heap + clase Order
├── test_priority_queue.py  # 15 unit tests
├── templates/
│   └── index.html          # Interfaz web
├── static/
│   └── style.css
└── README.md
```

---

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/orders` | Lista todas las órdenes en cola |
| POST | `/api/orders` | Agrega una nueva orden |
| POST | `/api/orders/dispatch` | Despacha la orden de mayor prioridad |
| PUT | `/api/orders/<id>/priority` | Actualiza la prioridad de una orden |
| DELETE | `/api/orders/<id>` | Cancela una orden |
| POST | `/api/orders/wait` | Suma minutos de espera a todas las órdenes |
| GET | `/api/history` | Historial de órdenes despachadas |
