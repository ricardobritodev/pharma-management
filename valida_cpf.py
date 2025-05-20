def valida_cpf():
    # Validador de CPF
    cpf = input('Digite seu CPF:\n>>> ')

    if cpf == "":
        print('Saindo...\n')
    else:
        digito_1 = int(cpf[0]) * 10
        digito_2 = int(cpf[1]) * 9
        digito_3 = int(cpf[2]) * 8
        digito_4 = int(cpf[3]) * 7
        digito_5 = int(cpf[4]) * 6
        digito_6 = int(cpf[5]) * 5
        digito_7 = int(cpf[6]) * 4
        digito_8 = int(cpf[7]) * 3
        digito_9 = int(cpf[8]) * 2
        digito_verificador = int(cpf[9])

        soma = (
            digito_1 + digito_2 + digito_3 + digito_4 + digito_5 +
            digito_6 + digito_7 + digito_8 + digito_9
        )

        multiplicado = soma * 10
        resto_divisao = multiplicado % 11

        if resto_divisao == 10:
            resto_divisao = 0

        print('Validando CPF..')

        if resto_divisao == digito_verificador:
            print('CPF Válido!')
        else:
            print('CPF INVÁLIDO!!!')
            print('Digite um CPF Válido.. >> ')
        
valida_cpf()

    
    