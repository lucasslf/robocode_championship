package lucasslf.battle_service.domain;

import java.net.URL;
import java.util.UUID;

public class Robot {
    private UUID id;
    private String name;
    private String url;


    public Robot(UUID id, String name, String url) {
        this.id = id;
        this.name = name;
        this.url = url;
    }

    public UUID getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getUrl() {
        return url;
    }

    public String getFileName(){
        return url.substring(url.lastIndexOf('/')+1);
    }

    @Override
    public String toString() {
        return "Robot{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", url='" + url + '\'' +
                '}';
    }
}
