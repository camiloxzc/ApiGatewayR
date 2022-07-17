# Contribuciones
## Clonar el proyecto en local

```
git clone https://github.com/camiloxzc/ApiGatewayR.git

```

## Cómo guardo mis cambios en el repositorio?

Primero guardo mis cambios en local y luego los agrego al repositorio
```
git add .
git commit -m "mensaje con el que identifico mis cambios"
git push origin master:nombre_de_mi_rama
```

Después de esto ingresa a este Git y debes hacer el pull request. La url debe ser algo como

```
https://github.com/camiloxzc/ApiGatewayR.git/pull/new/nombre_de_mi_rama
```

## Cómo hago si ya he trabajado pero mis compañeros ya han hecho algo?
En este caso es muy común y debes actualizar tu colaboración con lo que ya se ha hecho entes de subir tus cambios.
> Recuerda guardar tus cambios el local antes de cualquier cosa

```
git add .
git commit -m "mensaje con el que identifico mis cambios"
git pull --rebase origin master
```

Ya actualizado puedes subir los cambios en conjunto
```
git push origin master:nombre_de_mi_rama
```
# No tengo permiso para hacer cambios!!
Solo dilo por whatsapp a Francisco Martínez [martinezfran19 ]

# Instalation

```
$ pip install -r requirements.txt
```

# Running and test

```
$ python main.py
```
