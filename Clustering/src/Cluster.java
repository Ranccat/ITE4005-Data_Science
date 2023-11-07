import java.util.ArrayList;
import java.util.List;

public class Cluster {
    public Cluster(int idx) {
        pointList = new ArrayList<>();
        id = idx;
    }
    List<Point> pointList;
    int id;
}
