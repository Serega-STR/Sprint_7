class Data:
    # заведомо валидные данные, позволяющие создать пользователя
    login = 'yeylnsgmhw'
    password = 'gyexpkreef'
    first_name = 'yfnfesrvzi'
    
    payload_valid = {
        "login" : login, 
        "password" : password, 
        "firstName" : first_name
        }
    
    payload_with_empty_field = [
        {"login" : "", "password" : password},
        {"login" : login, "password" : ''},
        {"login" : login, "password" : None},
        {"login" : None, "password" : password},
        {},
        {'login' : login},
        {'password' : password}
    ]

    payload_without_login = [
        {'password' : password}
    ]

    payload_with_empty_login_field = [
        {"login" : "", "password" : password},
        {"login" : None, "password" : password},
        {"login" : login, "password" : ''},
        {'password' : password}
    ]
    
    payload_wrong_credentials = [
        # пробел в логине
        {"login" : " ", "password" : password},
        {"login" : " " + login, "password" : password},
        {"login" : login[:5] + " "+ login[5:], "password" : password},
        {"login" : login + " ", "password" : password},
        # пробел в пароле
        {"login" : login, "password" : " "},
        {"login" : login, "password" : " " + password},
        {"login" : login, "password" : password[:5] + ' ' + password[5:]},
        {"login" : login, "password" : password + " "},
        # число символов валидного логина, отличное от 10
        {"login" : login[0], "password" : password},
        {"login" : login[:2], "password" : password},
        {"login" : login[:5], "password" : password},
        {"login" : login[:8], "password" : password},
        {"login" : login[:9], "password" : password},
        {"login" : login + login[0], "password" : password},
        {"login" : login + login[0:2], "password" : password},
        {"login" : login + login[0:5], "password" : password},
        {"login" : login*2, "password" : password},
        # число символов валидного пароля, отличное от 10
        {"login" : "yeylnsgmhw", "password" : password[0]},
        {"login" : "yeylnsgmhw", "password" : password[:2]},
        {"login" : "yeylnsgmhw", "password" : password[:5]},
        {"login" : "yeylnsgmhw", "password" : password[:8]},
        {"login" : "yeylnsgmhw", "password" : password[:9]},
        {"login" : "yeylnsgmhw", "password" : password + password[0]},
        {"login" : "yeylnsgmhw", "password" : password + password[0:2]},
        {"login" : "yeylnsgmhw", "password" : password + password[0:5]},
        {"login" : "yeylnsgmhw", "password" : password*2},
        # логин / пароль с валидными символами, но нарушенной последовательностью
        {"login" : login[::-1], "password" : password},
        {"login" : login, "password" : password[::-1]},
        # логин / пароль CAPS'ом
        {"login" : login.upper(), "password" : password},
        {"login" : login, "password" : password.upper()}
    ]

    color = [
        None,
        [],
        [""],
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        ["GREY", "BLACK"]
    ]

    order_payload = {
            "firstName": "ivan",
            "lastName": "ivanov",
            "address": "Piter, Lenina д.1 кв. 5",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-05-06",
            "comment": "comment"
                }