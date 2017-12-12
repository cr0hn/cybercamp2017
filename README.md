# Código de ejemplo y scripts de Cybercamp 2017

# Gestión de credenciales

Es una buena práctica gestionar las credenciales como variable de entorno. Resulta más sencillo en el despliegue y, además, no insertamos información sensible en nuestro código fuente.

Para el trabajo en local, es habitual usar un fichero con nombre **.env**. El fichero tendrá el siguiente formato:

```bash
# File .env

export CF_API_EMAIL=XXXXX
export CF_API_KEY=XXXXXX
``` 

# Dominios

## Variable de entorno necesarias:

Tras registrar nuestra cuenta de Cloudflare, iremos a nuestra sección privada y obtendremos el API Key. El fichero **.env** debería ser similar a:

```bash
# File .env
export CF_API_EMAIL=your@mail.com
export CF_API_KEY=-----YOUR-AKI-KEY--------
```

## Instalar cloudflare_create_domain

El código de cloudflare_create_domain.py lo podéis descargar desde este mismo repositorio. Su instalación es muy sencilla

```bash
> python -m pip install -r requirements.txt 
> python cloudflare_create_domain.py -h
```

## Crear dominio:

```bash
> source .env
> python cloudflare_create_domain.py add my-new-domain.cr0hn.com
```

## Borrar dominio:

```bash
> python cloudflare_create_domain.py add my-new-domain.cr0hn.com
```

# Rancher

## Instalar Rancher-cli

El CLI de Rancher se puede descargar desde el propio portal de Rancher. Debajo, a la derecha tenéis los enlaces de descarga.

En los siguientes pasos tratamos de obtener de forma dinámica los puertos ocupados por los balanceadores desplegados en Rancher. Después, usaremos esta información para lanzar, usando una plantilla, un nuevo servicio en un puerto libre: 

## Variables de entorno necesarias:

Tras descargar el cliente, iremos a nuestra sección privada y obtendremos el API Key. El fichero **.env** debería ser similar a:

```bash
# File .env
export RANCHER_URL=https://myrancher-panel.eu
export RANCHER_ACCESS_KEY=XXXXXXXXXX
export RANCHER_SECRET_KEY=YYYYYYYYYYYYYYYYYYYY
```

## Obtener los balanceadores

```bash 
> LOAD_BALANCER=$(./rancher ps | grep -i LoadBalancers/SitesLoadBalancer | awk '{print $1}')
```

## Obtener los puertos del balanceador

```bash
> LB_PORTS=$(./rancher inspect $LOAD_BALANCER)
```

## Obtener todos los puertos ocupados del balanceador

```bash
> CURRENT_LB_PORTS=$(python -c "import json; ports=json.loads('$LB_PORTS')['launchConfig']['ports']; print(','.join(x.split(':')[0] for x in ports))")
```

## Obtener puerto libre en el balanceador

```bash
> SELECTED_FREE_PORT=$(python -c "import random; busy_ports='$CURRENT_LB_PORTS'; aval_ports=[x for x in range(1024, 65535) if str(x) not in busy_ports]; print(aval_ports[random.randint(0, len(aval_ports))])")
```

## Configurar las respuestas para nuestro catálogo

Para este ejemplo se ha escogido las respuestas para el catálogo de Wordpress. Así generaremos las respuestas:

```bash
> cat > answers.txt << EOF
public_port=$SELECTED_FREE_PORT
mariadb_root_password=mariadb_my_root
mariadb_user=wordpress_user
mariadb_user_password=wordpress_password
mariadb_database_name=bitnami_wordpress
wordpress_username=admin
wordpress_password=bitnami
volume_driver=local
EOF
```

## Lanzar catálogo

```bash
> ./rancher catalog install --answers answers.txt --name mywordpress community/wordpress:v0.2-bitnami
```

