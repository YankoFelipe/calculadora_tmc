# calculadora_tmc

## Problem description [Spanish]

Tu desafío es que construyas una aplicación que a partir de las las características de un crédito (monto y plazo), nos muestre la TMC que corresponde. Dado que la TMC cambia día a día queremos poder consultar por la TMC de cualquier día en particular.

El sistema debe responder realizando lo siguiente:
El usuario de la aplicación debe poder especificar el monto en UF, el plazo en días y la fecha en la que quieres saber la TMC.
Según esos parámetros la aplicación debe entregar la TMC correspondiente al día consultado.

## Dependencies
[requests](https://realpython.com/python-requests/)

## Assumptions about SBIF's API

### 1
The member 'Subtitulo' only says 'unidades de fomento' if is the UF case.

### 2
The lower bound comes after the string 'uperiores al equivalente de '

### 3
The upper bound comes after the string 'nferiores o iguales al equivalente de '

### 4
If no 'Hasta' is provided it will be assumed that the tmc is valid for one month

### 5
The credit can be only one of the followings: 'No reajustable', 'Reajustable' or 'Moneda extranjera'
