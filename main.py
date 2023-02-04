import matplotlib.pyplot as plt
import networkx as nx

# Выбор площадки для строительства аэропорта

# Варианты (млн., мин., тыс.)
A = [180, 70, 10]
B = [170, 40, 15]
C = [160, 55, 20]
D = [150, 50, 25]

p_1 = 3
p_2 = 2
p_3 = 1


# index - num of criteria, max - True, min - False
direction_for_criteria = [False, False, False]

all_consent_edges = list()
all_inconsent_edges = list()

# Метод возвращает множество оцениваемых объектов
# Затраты - min (p_1 = 3)
# Расстояние от города – min (p_2 = 2)
# Численность населения, подверженного шумовому влиянию – min (p_3 = 1)
def get_set_of_evaluated_objects(*data):
    return [data[i] for i in range(len(data))]


# Минимальное значение для заданных значений
def min_value(data):
    return min(data)


# Максимальное значение для заданных значений
def max_value(data):
    return max(data)


# Нормализация данных
def data_normalization(data, arr_of_base_value):
    for j in range(len(arr_of_base_value)):
        for i in range(len(data)):
            if direction_for_criteria[j]:
                if arr_of_base_value[j] != 0:
                    data[i][j] = round(data[i][j] / arr_of_base_value[j], 2)
            else:
                if data[i][j] != 0:
                    data[i][j] = round(arr_of_base_value[j] / data[i][j], 2)


# Список базовых значений для каждого столбца
def array_of_base_cow_values(data):
    array_of_base_elem = list()
    for j in range(len(data[0])):
        if direction_for_criteria[j]:
            array_of_base_elem.append(max_value([data[i][j] for i in range(len(data))]))
        else:
            array_of_base_elem.append(min_value([data[i][j] for i in range(len(data))]))

    return array_of_base_elem


# Cумма весов критериев
def sum_of_criteria(*value_of_criteria):
    return sum(value_of_criteria)


def get_edges_for_one_criteria(data, nodes, direction):
    array_of_edges = list()
    array_of_inconsent_edges = list()
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if direction:
                if data[i] > data[j]:
                    array_of_edges.append((nodes[i], nodes[j]))
                elif data[i] == data[j]:
                    array_of_edges.append((nodes[i], nodes[j]))
                    array_of_edges.append((nodes[j], nodes[i]))
                else:
                    array_of_inconsent_edges.append((nodes[i], nodes[j]))
            else:
                if data[i] < data[j]:
                    array_of_edges.append((nodes[j], nodes[i]))
                elif data[i] == data[j]:
                    array_of_edges.append((nodes[i], nodes[j]))
                    array_of_edges.append((nodes[j], nodes[i]))
                else:
                    array_of_inconsent_edges.append((nodes[j], nodes[i]))


    for i in range(len(nodes) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            if direction:
                if data[i] > data[j]:
                    array_of_edges.append((nodes[i], nodes[j]))
                elif data[i] == data[j]:
                    array_of_edges.append((nodes[i], [j]))
                    array_of_edges.append((nodes[j], [i]))
                else:
                    array_of_inconsent_edges.append((nodes[i], nodes[j]))
            else:
                if data[i] < data[j]:
                    array_of_edges.append((nodes[j], nodes[i]))
                elif data[i] == data[j]:
                    array_of_edges.append((nodes[i], nodes[j]))
                    array_of_edges.append((nodes[j], nodes[i]))
                else:
                    array_of_inconsent_edges.append((nodes[j], nodes[i]))

    return array_of_edges, array_of_inconsent_edges


def draw_graph(graph):
    # рисуем граф и отображаем его
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


def get_relationship_graph(data, direction):
    graph = nx.DiGraph()
    graph_in = nx.DiGraph()

    # определяем список узлов (ID узлов)
    nodes = [chr(65 + i) for i in range(len(data))]

    # определяем список рёбер
    # список кортежей, каждый из которых представляет ребро
    # кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
    # Для каждого критерия i строим граф Gi = (X, Vi), где Vi - множество дуг графа Gi.
    # Дуга в графе Gi из вершины х в вершину у существует, если x_i ≥ y_i.
    # Равенство оценок x_i = y_i в графе влечет наличие двух дуг из х в у и из у в х.
    # (x,y) Є Vi ó xi ≥ yi, i = 1..n.
    edges, in_edges = get_edges_for_one_criteria(data, nodes, direction)

    # добавляем информацию в объект графа
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    all_consent_edges.append(edges)
    all_inconsent_edges.append(in_edges)

    graph_in.add_nodes_from(nodes)
    graph_in.add_edges_from(in_edges)


    draw_graph(graph)
    draw_graph(graph_in)


def get_criteria_graphs(data, direction_for_criteria):
    for j in range(len(data[0])):
        temp_data = [data[i][j] for i in range(len(data))]
        get_relationship_graph(temp_data, direction_for_criteria[j])


def get_matrix_of_consent_indices(data, criteria):
    N = len(data)
    matrix = [[0 for _ in range(N)] for __ in range(N)]

    for crit in range(len(all_consent_edges)):
        for elem in all_consent_edges[crit]:
            matrix[ord(elem[1]) - 65][ord(elem[0]) - 65] += criteria[crit]

    return matrix


def matrix_normalization_of_criteria(matrix, sum_of_criteria):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = round(matrix[i][j] / sum_of_criteria, 2)


def get_the_normalizing_coefficient(data, criteria):
    result = list()
    for j in range(len(criteria)):
        result.append(round(max_value([data[i][j] for i in range(len(data))]) - min_value([data[i][j] for i in range(len(data))]), 2))

    return result


def max_difference_in_criteria(data, first, last, scales):
    diff = list()
    for j in range(len(data[0])):
        diff.append(data[last][j] - data[first][j])

    max = diff[0] / scales[0]
    for i in range(1, len(diff)):
        if diff[i] / scales[i] > max:
            max = diff[i] / scales[i]

    return max


def get_inconsistency_matrix(data, scales):
    N = len(data)
    matrix = [[0 for _ in range(N)] for __ in range(N)]

    for i in range(len(all_inconsent_edges)):
        for elem in all_inconsent_edges[i]:
            matrix[ord(elem[0]) - 65][ord(elem[1]) - 65] = round(max_difference_in_criteria(data, ord(elem[1]) - 65, ord(elem[0]) - 65, scales), 2)

    return matrix


if __name__ == '__main__':
    data = get_set_of_evaluated_objects(A, B, C, D)
    print('Данные {}'.format(data))
    # data_normalization(data, array_of_base_cow_values(data))
    #print('Нормализованные данные {}'.format(data))

    criteria = [p_1, p_2, p_3]
    print('Значения критериев {}'.format(criteria))

    get_criteria_graphs(data, direction_for_criteria)
    print('Все ребра графов отношений {}'.format(all_consent_edges))

    matrix = get_matrix_of_consent_indices(data, criteria)
    matrix_normalization_of_criteria(matrix, sum_of_criteria(p_1, p_2, p_3))

    L_1 = 100
    L_2 = 50
    L_3 = 45

    scales = [L_1, L_2, L_3]

    in_matrix = get_inconsistency_matrix(data, scales)

    print("Матрица согласования {}".format(matrix))
    print("Матрица несогласования {}".format(in_matrix))