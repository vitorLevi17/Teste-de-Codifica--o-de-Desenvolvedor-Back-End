from fastapi import HTTPException, status
def validar_objeto_bd(objeto,objeto_id):
    if objeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {objeto_id} não encontrado"
        )