from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def cliente():
    clientes = [{
               'ID':1,
               'Cliente':'Vitor',
               'Telefone':'71 999998888',
               'Email':'vitor@gmail.com',
               'CPF':'00000000011',
               },
               {'ID':2,
                'Cliente': 'Vitoria',
                'Telefone': '71 989998888',
                'Email': 'vitoria@gmail.com',
                'CPF': '00000000022'
                },
               ]
    return clientes