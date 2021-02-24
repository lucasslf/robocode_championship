package lucasslf.battle_service.infra;

import lucasslf.battle_service.domain.Robot;

import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.FileChannel;
import java.nio.channels.ReadableByteChannel;

public class RobotDownloader {

    public static final String BASE_DIR = "robots";

    public static void downloadRobot(Robot robot){

        String fileName = BASE_DIR+"/"+robot.getFileName();

        try {
            System.out.println("Downloading");
            System.out.println(fileName);
            System.out.println(robot.getUrl());
            URL url = new URL(robot.getUrl().replace("localhost", "robot-service"));

            ReadableByteChannel readableByteChannel = Channels.newChannel(url.openStream());
            FileOutputStream fileOutputStream = new FileOutputStream(fileName);
            FileChannel fileChannel = fileOutputStream.getChannel();
            fileChannel.transferFrom(readableByteChannel, 0, Long.MAX_VALUE);
        }catch (IOException ex){
            System.out.println("Error");
            System.out.println(ex.getMessage());
        }
    }

}
