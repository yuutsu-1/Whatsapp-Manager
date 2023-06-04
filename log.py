import os
import time

def format_message(message: str) -> str:
    msg_l = message.split(" ")
    new = []
    for x in msg_l:
        if "\n" in x:
            x = x.replace("\n", "")
            new.append(x) if not len(x) == 0 else None

        elif len(x) != 0:
            new.append(x)

    return " ".join(new)


def log_message(_time: time.struct_time, receiver: str, message: str) -> None:

    if not os.path.exists("logErro.txt"):
        file = open("logErro.txt", "w+")
        file.close()

    message = format_message(message)

    with open("logErro.txt", "a", encoding="utf-8") as file:
        file.write(
            f"Data: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nHora: {_time.tm_hour}:{_time.tm_min}\n"
            f"Numero de telefone: {receiver}\nMensagem: {message}"
        )
        file.write("\n--------------------\n")
        file.close()
