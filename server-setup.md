# Базовая настройка сервера (Hardening)

Эта инструкция описывает первичную настройку "голого" Linux-сервера для проекта AutoParts Store.

## 1. Беспарольный доступ по SSH
Для безопасности мы используем вход по SSH-ключам вместо паролей.

* Генерация ключа (современный алгоритм ed25519):
  `ssh-keygen -t ed25519`
* Копирование публичного ключа на сервер:
  `ssh-copy-id user@<IP_сервера>`

## 2. Настройка безопасности SSH (sshd_config)
Редактируем файл `/etc/ssh/sshd_config` (нужны права sudo):
* `PasswordAuthentication no` — полный запрет входа по паролю (защита от брутфорса).
* `PermitRootLogin no` — запрет прямого входа под суперпользователем root.

После изменений обязательно перезапускаем службу:
`sudo systemctl restart ssh`

## 3. Настройка Firewall (UFW)
Закрываем все порты, кроме тех, что нужны для работы.
* Разрешаем SSH (чтобы не потерять доступ): `sudo ufw allow 22/tcp`
* Включаем файрвол: `sudo ufw enable`
* Проверяем статус: `sudo ufw status`

## 4. Настройка автозапуска сервиса (Systemd)
Чтобы наше API работало в фоне и само восстанавливалось после сбоев, мы создали systemd-юнит.

Файл конфигурации: `sudo nano /etc/systemd/system/autoparts.service`
Содержимое:
[Unit]
Description=AutoParts Store Backend API
After=network.target

[Service]
User=dracula
WorkingDirectory=/home/dracula/backend
ExecStart=/usr/bin/python3 /home/dracula/backend/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

Команды управления:
* `sudo systemctl daemon-reload` — перечитать конфиги
* `sudo systemctl enable autoparts` — добавить в автозагрузку
* `sudo systemctl start autoparts` — запустить сейчас
* `sudo systemctl status autoparts` — проверить статус
* `sudo journalctl -u autoparts -f` — смотреть логи в реальном времени