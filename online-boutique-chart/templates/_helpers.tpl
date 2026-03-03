{{/*
  _helpers.tpl - Template helpers cho Online Boutique Helm Chart
  Quy tắc đặt tên: [service]-online-boutique
*/}}

{{/* Tạo tên đầy đủ cho resource theo pattern [service]-online-boutique */}}
{{- define "online-boutique.fullname" -}}
{{- printf "%s-online-boutique" .service }}
{{- end }}

{{/* Namespace của chart */}}
{{- define "online-boutique.namespace" -}}
{{- .Values.namespace | default "online-boutique" }}
{{- end }}

{{/* imagePullSecrets block */}}
{{- define "online-boutique.imagePullSecrets" -}}
imagePullSecrets:
{{- range .Values.imagePullSecrets }}
  - name: {{ .name }}
{{- end }}
{{- end }}

{{/* initContainer: chờ 1 host:port bằng nc -z */}}
{{- define "online-boutique.initWait" -}}
- name: wait-for-{{ .name }}
  image: busybox:1.36
  imagePullPolicy: IfNotPresent
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop: ["ALL"]
    privileged: false
    readOnlyRootFilesystem: true
  command:
    - sh
    - -c
    - |
      echo "Waiting for {{ .host }}:{{ .port }}..."
      until nc -z {{ .host }} {{ .port }}; do
        echo "  ...not ready, sleeping 3s"
        sleep 3
      done
      echo "{{ .host }}:{{ .port }} is UP!"
{{- end }}
