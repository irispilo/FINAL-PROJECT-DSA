class Order:
    def __init__(self, order_id, customer, items, order_type, priority=None):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.order_type = order_type  # 'express', 'mesa', 'para_llevar'
        self.wait_time = 0  # minutos esperando
        self.priority = priority if priority is not None else self._calculate_priority()

    def _calculate_priority(self):
        base = {"express": 30, "para_llevar": 20, "mesa": 10}
        return base.get(self.order_type, 10) + self.wait_time

    def update_wait(self, minutes):
        self.wait_time += minutes
        self.priority = self._calculate_priority()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer": self.customer,
            "items": self.items if isinstance(self.items, str) else ", ".join(self.items),
            "order_type": self.order_type,
            "wait_time": self.wait_time,
            "priority": self.priority,
        }


class MaxPriorityQueue:
    """
    Max-Heap based Priority Queue implementada desde cero.
    Complejidades temporales:
        insert         -> O(log n)
        extract_max    -> O(log n)
        peek           -> O(1)
        update_priority-> O(n) buscar + O(log n) heapify = O(n)
        delete         -> O(n) buscar + O(log n) heapify = O(n)
        size           -> O(1)
        is_empty       -> O(1)
        get_all        -> O(n)
    """

    def __init__(self):
        self._heap = []

    # ── helpers ───────────────────────────────────────────────────────────────

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _heapify_up(self, i):
        """Sube el nodo en posición i hasta restaurar la propiedad del heap."""
        while i > 0:
            p = self._parent(i)
            if self._heap[p].priority < self._heap[i].priority:
                self._swap(p, i)
                i = p
            else:
                break

    def _heapify_down(self, i):
        """Baja el nodo en posición i hasta restaurar la propiedad del heap."""
        n = len(self._heap)
        while True:
            largest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._heap[l].priority > self._heap[largest].priority:
                largest = l
            if r < n and self._heap[r].priority > self._heap[largest].priority:
                largest = r
            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def _find_index(self, order_id):
        """Busca el índice de una orden por su ID. O(n)."""
        for i, order in enumerate(self._heap):
            if order.order_id == order_id:
                return i
        return -1

    # ── core methods ──────────────────────────────────────────────────────────

    def insert(self, order: Order):
        """Inserta una orden y restaura el heap. O(log n)."""
        self._heap.append(order)
        self._heapify_up(len(self._heap) - 1)

    def extract_max(self):
        """Extrae y retorna la orden de mayor prioridad. O(log n)."""
        if self.is_empty():
            raise IndexError("La cola está vacía.")
        self._swap(0, len(self._heap) - 1)
        max_order = self._heap.pop()
        if not self.is_empty():
            self._heapify_down(0)
        return max_order

    def peek(self):
        """Retorna la orden de mayor prioridad sin extraerla. O(1)."""
        if self.is_empty():
            return None
        return self._heap[0]

    def update_priority(self, order_id, new_priority):
        """Actualiza la prioridad de una orden y reordena el heap. O(n)."""
        i = self._find_index(order_id)
        if i == -1:
            raise ValueError(f"Orden {order_id} no encontrada.")
        old = self._heap[i].priority
        self._heap[i].priority = new_priority
        if new_priority > old:
            self._heapify_up(i)
        else:
            self._heapify_down(i)

    def delete(self, order_id):
        """Elimina una orden de cualquier posición del heap. O(n)."""
        i = self._find_index(order_id)
        if i == -1:
            raise ValueError(f"Orden {order_id} no encontrada.")
        self._heap[i].priority = float("inf")
        self._heapify_up(i)
        return self.extract_max()

    def add_wait_time(self, minutes):
        """Incrementa el tiempo de espera de todas las órdenes y reconstruye el heap. O(n log n)."""
        for order in self._heap:
            order.update_wait(minutes)
        self._build_heap()

    def _build_heap(self):
        """Reconstruye el heap desde cero. O(n)."""
        n = len(self._heap)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(i)

    def is_empty(self):
        """O(1)."""
        return len(self._heap) == 0

    def size(self):
        """O(1)."""
        return len(self._heap)

    def get_all(self):
        """Retorna todas las órdenes ordenadas por prioridad (mayor a menor). O(n log n)."""
        return sorted(self._heap, key=lambda o: o.priority, reverse=True)
