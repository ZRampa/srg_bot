from datetime import datetime

arr = {1: "Кондратьєва Віра Василівна\nРожкова Марія Павлівна\n\nслужбовий телефон: 0442597180",
       2: "Марченко Ольга Григоровна\nМочарська Раїса Володимирівна\n\nслужбовий телефон: 0442597180",
       3: "Лиман Юлія Станіславівна\nКоваленко Татяна Анатолівна\n\nслужбовий телефон: 0442597180",
       4: "Золотнюк Татяна Святославівна\nБосак Галина Володимирівна\n\nслужбовий телефон: 0442597180"}


def days_between_dates():
    current_datetime = datetime.now()

    date_format = "%Y-%m-%d %H:%M:%S"
    start_datetime = datetime.strptime("2023-08-01 08:00:00", date_format)
    end_datetime = datetime.strptime(current_datetime.strftime("%Y-%m-%d %H:%M:%S"), date_format)
    # end_datetime = datetime.strptime("2023-08-05 08:00:00", date_format)
    days_passed = (end_datetime - start_datetime).days
    return days_passed


def get_vahta():
    day = days_between_dates()
    k = 1
    for i in range(0, day):
        if k == 4:
            k = 1
        else:
            k += 1

    return arr.get(k)
