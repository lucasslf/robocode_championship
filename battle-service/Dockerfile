FROM openjdk:11
VOLUME /tmp
ARG JAR_FILE=target/battle-service-0.0.1.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
EXPOSE 8081