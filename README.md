# PyLabs

# Lab1  (with 2.3)

1.0. Напишите программу, которая принимает 3 числа, сравнивает между собой и возвращает максимальное и минимальное числа. Программа должна также корректно обрабатывать различные варианты равенств чисел. Функции min и мах не использовать. Только условный оператор.

2.1. Напишите программу, в которой задается  натуральное число n и выводится обратная лестница из n ступенек, i-я ступенька должна состоять из чисел от 1 до i без пробелов.

2.2. Напишите программу, в которой задается натуральное число n и выводится перевернутая пирамида из n ступенек, i-я ступень должна состоять из чисел от 1 до i и обратно без пробелов.

2.3.* Обратите внимание что при решении заданий 2.1 и. 2.2 «в лоб», при выводе треугольника и пирамиды между строками 9 и 10, и далее на 99 и 100 будет наблюдаться излом на стороне связанный с переходом на числа большей разрядности. Модернизируйте код таким образом, чтобы треугольник и пирамида были правильными для любых чисел.
  
3.0. Напишите программу, которая выводит n строк треугольника Паскаля. https://ru.wikipedia.org/wiki/Треугольник_Паскаля
Число n вводится с клавиатуры.


# Lab2

1.0. Напишите программу, которая принимает на вход строку символов (заглавные и прописные буквы латинского алфавита), которые могут повторятся, например: YYYYggkeeeAAABV . Заглавные и строчные буквы различаются. Программа должна преобразовать (закодировать) строку в сжатый формат: Y4g2ke3A3BV . Число после символа – количество повторений, если символ однократный – едениwe выводить не надо.

1.1. Напишите программу, которая решает обратную задачу по отношению к заданию 1. Из строки типа  Y4g2ke3A3BV восстанавливает исходную.

2.0. Напишите программу,  которая выводит 3 наиболее часто встречающихся символа (без учета пробелов) с указанием их количества, в введенной пользователем строке

3.0. Напишите программу,  которая выводит текстовое написание числа. Число вводится пользователем в диапазоне от 1 до 1000. Например, при вводе числа 17 – выводится «семнадцать».

# Lab3

Задание 0
Задан список с числами. Напишите программу, которая выводит все элементы списка, которые больше предыдущего, в виде отдельного списка.

Задание 1
Задан список с числами. Напишите программу, которая меняет местами наибольший и наименьший элемент и выводит новый список.

Задание 2
Напишите программу, которая принимает 2 списка чисел и определяет количество общих чисел из первого и второго списка.

Задание 3
Напишите программу, которая принимает список строк и выводит количество повторений данных строк в списке.
Необходимо реализовать решение с использованием словарей.


# Lab4

Задание 1
Задан словарь. Напишите программу, которая будет выводить значение по заданному ключу.
Ключи, чьи значения необходимо найти, должны задаваться с помощью функции input(). Т.к. в данной задаче используется функция input(), получение значения ключей типа int не принципиально.

Задание 2
Напишите программу, которая будет выполнять действие, обратное заданию 1. Программа должна производить поиск по значению и выдавать ключ.

Задание 3
Напишите программу, которая принимает список строк и выводит количество повторений данных строк в списке.
Необходимо реализовать решение с использованием словарей.


Задание 4
Дана строка в виде случайной последовательности чисел от 0 до 9. Требуется создать словарь, который в качестве ключей будет принимать данные числа (т. е. ключи будут типом int), а в качестве значений – количество этих чисел в имеющейся последовательности. Функция должна возвратить словарь из 3-х самых часто встречаемых чисел.


# Lab5

Задание 1
Считать из файла input.txt 10 чисел (числа записаны через пробел). Затем записать их произведение в файл output.txt.

Задание 2
Дан файл в котором записаны в столбик (каждое на отдельной строке) целые числа, всего 10 чисел. Отсортировать их по возрастанию цифр и записать в другой файл.

Задание 3
В текстовом файле записаны сведения о детях из детского сада в следующей форме (создать не менее 5 записей, с разным возрастом):
Фамилия пробел Имя пробел возраст
Иванов Иван 5 
Необходимо записать в отдельные текстовые файлы самого старшего и самого младшего



# Lab 5

Задание 1
Считать из файла input.txt 10 чисел (числа записаны через пробел). Затем записать их произведение в файл output.txt.

Задание 2
Дан файл в котором записаны в столбик (каждое на отдельной строке) целые числа, всего 10 чисел. Отсортировать их по возрастанию цифр и записать в другой файл.

Задание 3
В текстовом файле записаны сведения о детях из детского сада в следующей форме (создать не менее 5 записей, с разным возрастом):
Фамилия пробел Имя пробел возраст
Необходимо записать в отдельные текстовые файлы самого старшего и самого младшего

# Lab6

Написать программу на Python преобразующую json файл  в CSV. Входной параметр  – имя json файла. Результирующий CSV файл должен иметь название из названия записи json и размещаться  в той же папке что и  json.
Формат вызова программы в командной строке:  json2csv.py example.json

# Lab7

 Для файла _1.js создать схему документа, написать код валидации файла по
созданной схеме. На базе исходного файла сделать файл с ошибкой, показать
(вывести на экран) что файл валидацию не проходит. В отчете по заданию кроме
исходного файла должен быть код программы, схема js файла, неправильный
вариант файла

 Файл _2.js хранит данные о пользователях. Вначале необходимо с помощью
JSONF rmtt привести файл к читабельному виду. Далее необходимо извлечь в
словарь и вывести на экран следующие данные о всех пользователях: ключи
имена позьзователей, значения- телефоны. Отчет должен содержать файл с
вашим кодом и читабельный исходный файл.

 В данном задании необходимо внести исправления в файл _3.js следующего
плана: необходимо добавить как минимум 1 обьект в массив Inv i (придумать
для него разумные данные). Сохранить новый файл в формате JSON. Отчет
должен содержать код и новый JSON фай

# Lab8

Написать программу которая:
·	Загружает csv файл (файл прилагается к заданию)
Необходимо реализовать следующий функционал:
·	Функция Show()
Выводит файл на экран в визуально разборчивом варианте (как минимум выделить столбцы) и заголовки 
Опции функции:
Параметр: тип вывода, варианты: top - с начала таблицы (по умолчанию), bottom  - с конца таблицы, random - случайным образом
Целое число – количество выводимых строк, по умолчанию выводится 5 строк (соответственно 5 первых, 5 последних, 5 случайных). Если данных меньше 5 строк  - вывести все и сообщить что строк недостаточно
Разделитель – по умолчанию - запятая, но используя параметр separator = ‘ ‘ можно задать свой
·	Функция Info()
Выводит элементарную статистику о файле:
o	Количество строк с данными (строку с заголовком не считать) и количество колонок в таблице , в виде: 100х18
o	Далее выводится список имен полей данных с количеством не пустых значений и типом значений(согласно типам данных Python):
	Qty        99  int
	Name  100  string
	............................
o	Пустым считается поле не содержащее данных – в файле  ,,
·	Функция  DelNaN()
Удаляет из данных все строки в которых есть пустые поля
·	Функция MakeDS()
Случайным образом делит данные (строки) в соотношении 70\30
Создает в месте расположения файла программы папку workdata, в ней создает 2 папки: Learning и Testing. В папку learning записывается файл содержащий 70% данных с именем train.csv  в папку testing записывается файл содержащий 30% данных с именем test.csv


# Lab9


1.	Сохранить этот текст в файл. Прочитать матрицу из файла.
Hайдите для этой матрицы сумму всех элементов, максимальный и минимальный элемент (число)
3,4,17,-3
5,11,-1,6
0,2,-5,8

2. Реализовать кодирование длин серий (Run-length encoding). Дан вектор x. Необходимо вернуть кортеж из двух векторов одинаковой длины. Первый содержит числа, а второй - сколько раз их нужно повторить. Пример: x = np.array([2, 2, 2, 3, 3, 3, 5]). Ответ: (np.array([2, 3, 5]), np.array([3, 3, 1])).

3. Написать программу NumPy генерирующую массив случайных чисел нормального распределения размера 10х4. Найти минимально, максимальное, средние значения, стандартное отклонение. Сохранить первые 5 строк в отдельную переменную.

4. Найти максимальный элемент в векторе x среди элементов, перед которыми стоит нулевой. Для x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0]) ответ 5.

5. Реализовать функцию вычисления логарифма плотности многомерного нормального распределения Входные параметры: точки X, размер (N, D), мат. ожидание m, вектор длины D, матрица ковариаций C, размер (D, D). Разрешается использовать библиотечные функции для подсчета определителя матрицы, а также обратной матрицы, в том числе в невекторизованном варианте. Сравнить с scipy.stats.multivariate_normal(m, C).logpdf(X) как по скорости работы, так и по точности вычислений.

6. Поменять местами две строки в двумерном массиве NumPy -  поменяйте  строки 1 и 3 массива а.  a = np.arange(16).reshape(4,4)

7. Найти уникальные значения и их количество в столбце species таблицы iris.
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype='object')

8. Найти индексы ненулевых элементов в [0,1,2,0,0,4,0,6,9]


# lab10

1.	Вывести на один график, разными цветами графики полиномов Лежандра различных степеней (от 1 до 7). Задать заголовок изображения как «Полиномы Лежандра». Реализовать легенду графика в виде выносок от каждого полинома на графике с указанием степени ( - n = 3 как пример). Для реализации полиномов использовать ScyPy.

2.	Реализовать на Python и отрисовать с помощью Matplotlib ряд из фигур Лисажу (4 графика) с разным соотношение частот (3:2), (3:4), (5:4), (5:6).

3.	Реализовать с помощью Matplotlib анимацию врашения фигуры Лисажу при нулевом сдвиге фаз и изменении соотношения частот от 0 до 1

4.	Реализовать с помощью Matplotlib блок моделирования сложения 2 волн, включающий 2 интерактивных окна для задания исходных волн (как sin(x)) минимальная интерактивность включат 2 слайдера регулирующих частоту и амплитуду волны. Кроме 2 интерактивных  окон должно присутствовать окно отображающее результат сложения 2х волн

5.	Отрисовать с помощью Matplotlib изображение включающее в себя 2 трехмерных графика функции среднеквадратичного отклонения MSE. На втором графике ось z реализовать в логарифмическом масштабе.

