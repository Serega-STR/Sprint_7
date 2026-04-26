class Data:
    # заведомо валидные данные, позволяющие создать пользователя
    login = 'yeylnsgmhw'
    password = 'gyexpkreef'
    first_name = 'yfnfesrvzi'
    reversed_login = login[::-1]
    reversed_password = password[::-1]
    
    payload_valid = {
        "login" : login, 
        "password" : password, 
        "firstName" : first_name
        }
    
    payload_with_empty_field = [
        {"" : "yeylnsgmhw", "password" : "gyexpkreef"},
        {"login" : "", "password" : "gyexpkreef"},
        {"login" : "yeylnsgmhw", "password" : None},
        {},
        {'login' : 'yeylnsgmhw'},
        {'password' : 'gyexpkreef'}
    ]

    payload_without_login = [
        {'password' : 'gyexpkreef'}
    ]

    payload_with_empty_login_field = [
        {"" : "yeylnsgmhw", "password" : "gyexpkreef"},
        {"login" : "", "password" : "gyexpkreef"},
        {"login" : None, "password" : "gyexpkreef"},
        {'password' : 'gyexpkreef'}
    ]
    #{"login" : "yeylnsgmhw", "password" : "gyexpkreef"},
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
        {"login" : reversed_login, "password" : password},
        {"login" : login, "password" : reversed_password}
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