## Booking hotels
Platform is an online platform for hotel owners. Designed to ease things up for more convenient hotel rooms booking.

## 🎯 Features
* Hotel rooms booking engine
* Tracking rooms availability status
* Receiving payments for room reservations (payment gateway)
* Customer review system

## ⚙️ Installation

Make sure you have Python installed ([download](https://www.python.org/downloads/)). Version `3.7` or higher is required.  

```bash
# install requirements
$ pip install -r requirements.txt
```

## ⚡️ Getting started

Start application:
```bash
$ python manage.py runserver
```
Application service will be available on `localhost:8000`

## How it works
Project built on `Python/Django`. `MySQL` database stores hotels data. App is split by two client sides: hotel management system - for hotel owners and booking engine page - for customers. Platform is a `RESTfull` application that allows to change and retrieve hotel data. For each hotel `token` is created and allows to implement program interface for third party applications. 


### Screenshots
![hoteladminsystem](https://user-images.githubusercontent.com/40773987/159276577-e5107d1d-6325-48ad-880b-9270c7e50855.png)
![bookingpage](https://user-images.githubusercontent.com/40773987/159276656-7582ada1-59ec-454f-a0f7-e3620cb71869.png)


