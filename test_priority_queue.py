import pytest
from priority_queue import MaxPriorityQueue, Order


def make_order(oid, otype="mesa", priority=None):
    return Order(oid, "Test User", "Pizza", otype, priority)

'''
Order("A", "Test User", "Pizza", "mesa", 10)
Order("B", "Test User", "Pizza", "mesa", 20)
Order("C", "Test User", "Pizza", "express", 30)

'''

@pytest.fixture
def pq():
    return MaxPriorityQueue()


# 1. Cola vacía
def test_empty_queue(pq):
    assert pq.is_empty()
    assert pq.size() == 0


# 2. Insertar un elemento
def test_insert_single(pq):
    pq.insert(make_order("A", priority=10))
    assert not pq.is_empty()
    assert pq.size() == 1


# 3. Peek devuelve el máximo sin extraer
def test_peek_returns_max(pq):
    pq.insert(make_order("A", priority=10))
    pq.insert(make_order("B", priority=50))
    pq.insert(make_order("C", priority=30))
    assert pq.peek().order_id == "B"
    assert pq.size() == 3


# 4. Extract_max devuelve siempre el mayor
def test_extract_max_order(pq):
    pq.insert(make_order("A", priority=10))
    pq.insert(make_order("B", priority=50))
    pq.insert(make_order("C", priority=30))
    assert pq.extract_max().order_id == "B"
    assert pq.extract_max().order_id == "C"
    assert pq.extract_max().order_id == "A"


# 5. Extract_max en cola vacía lanza excepción
def test_extract_empty_raises(pq):
    with pytest.raises(IndexError):
        pq.extract_max()


# 6. Update priority hacia arriba
def test_update_priority_up(pq):
    pq.insert(make_order("A", priority=10))
    pq.insert(make_order("B", priority=20))
    pq.update_priority("A", 99)
    assert pq.peek().order_id == "A"


# 7. Update priority hacia abajo
def test_update_priority_down(pq):
    pq.insert(make_order("A", priority=50))
    pq.insert(make_order("B", priority=20))
    pq.update_priority("A", 5)
    assert pq.peek().order_id == "B"


# 8. Update priority en orden inexistente lanza excepción
def test_update_nonexistent_raises(pq):
    with pytest.raises(ValueError):
        pq.update_priority("NO-EXISTE", 99)


# 9. Delete elimina la orden correcta
def test_delete_order(pq):
    pq.insert(make_order("A", priority=10))
    pq.insert(make_order("B", priority=50))
    pq.insert(make_order("C", priority=30))
    deleted = pq.delete("B")
    assert deleted.order_id == "B"
    assert pq.size() == 2
    assert pq.peek().order_id == "C"


# 10. Delete en orden inexistente lanza excepción
def test_delete_nonexistent_raises(pq):
    with pytest.raises(ValueError):
        pq.delete("NO-EXISTE")


# 11. Get_all retorna todas ordenadas por prioridad
def test_get_all_sorted(pq):
    priorities = [15, 40, 5, 60, 25]
    for i, p in enumerate(priorities):
        pq.insert(make_order(str(i), priority=p))
    result = [o.priority for o in pq.get_all()]
    assert result == sorted(priorities, reverse=True)


# 12. Prioridad automática por tipo de orden
def test_priority_by_type():
    express = make_order("E", "express")
    mesa = make_order("M", "mesa")
    llevar = make_order("L", "para_llevar")
    assert express.priority > llevar.priority
    assert llevar.priority > mesa.priority


# 13. add_wait_time aumenta prioridad y reordena
def test_wait_time_increases_priority(pq):
    pq.insert(make_order("A", "mesa"))
    pq.insert(make_order("B", "express"))
    old_priority = pq._heap[0].priority
    pq.add_wait_time(10)
    assert pq._heap[0].priority > old_priority


# 14. Heap mantiene propiedad después de múltiples inserciones
def test_heap_property_after_inserts(pq):
    import random
    vals = random.sample(range(1, 100), 20)
    for v in vals:
        pq.insert(make_order(str(v), priority=v))
    extracted = []
    while not pq.is_empty():
        extracted.append(pq.extract_max().priority)
    assert extracted == sorted(extracted, reverse=True)


# 15. Size decrementa correctamente tras operaciones
def test_size_after_operations(pq):
    for i in range(5):
        pq.insert(make_order(str(i), priority=i))
    assert pq.size() == 5
    pq.extract_max()
    assert pq.size() == 4
    pq.delete("2")
    assert pq.size() == 3