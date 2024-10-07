FROM provectuslabs/kafka-ui:v0.7.1

USER root
# install gcc
RUN apk add --no-cache gcc musl-dev
COPY flag.txt health.c /
RUN gcc -o health health.c && chown root:root health && chmod 4755 health
RUN chown root:root /flag.txt && chmod 400 /flag.txt
USER kafkaui

