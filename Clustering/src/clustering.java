import java.util.*;
import java.io.*;

public class clustering {
    public static List<Point> db = new ArrayList<>();
    public static List<Cluster> clusters = new ArrayList<>();
    public static int n;
    public static int Eps;
    public static int MinPts;
    public static int inputNum;
    public static int maxInputNum;
    private static final int UNDEFINED = 0;
    private static final int NOISE = -1;

    public static void main(String[] args) throws Exception {
        // Parameters
        String fileName = args[0];
        n = Integer.parseInt(args[1]);
        Eps = Integer.parseInt(args[2]);
        MinPts = Integer.parseInt(args[3]);

        // Finding .txt Number
        maxInputNum = 100;
        inputNum = 0;
        while (true) {
            if (inputNum > maxInputNum) {
                break;
            }
            if (fileName.contains(String.valueOf(inputNum))) {
                break;
            }
            inputNum++;
        }

        // Reading Files To DB
        BufferedReader reader = new BufferedReader(new FileReader(fileName));
        String str;
        String[] tokens;
        while ((str = reader.readLine()) != null) {
            tokens = str.split("\t");
            int id = Integer.parseInt(tokens[0]);
            double x = Double.parseDouble(tokens[1]);
            double y = Double.parseDouble(tokens[2]);

            Point point = new Point(id, x, y);
            db.add(point);
        }

        // DBSCAN
        int index = -1;
        for (Point p : db) {
            if (p.label != UNDEFINED) continue;
            List<Point> neighbors = findNeighbor(p);
            if (neighbors.size() < MinPts) {
                p.label = NOISE;
                continue;
            }
            Cluster c = new Cluster(++index);
            p.label = c.id;
            c.pointList.add(p);
            HashSet<Point> seed = new HashSet<>(neighbors);
            HashSet<Point> nextSeed = new HashSet<>();
            seed.remove(p);
            c.pointList.addAll(new ArrayList<>(seed));

            while (true) {
                for (Point q : seed) {
                    if (q.label == NOISE) {
                        q.label = c.id;
                        c.pointList.add(q);
                    }
                    if (q.label != UNDEFINED) {
                        continue;
                    }
                    List<Point> N = findNeighbor(q);
                    q.label = c.id;
                    c.pointList.add(q);
                    if (N.size() < MinPts) {
                        continue;
                    }
                    nextSeed.addAll(new HashSet<>(N));
                }
                nextSeed.removeAll(new HashSet<>(c.pointList));
                if (nextSeed.size() == 0) {
                    break;
                }
                seed = nextSeed;
                nextSeed = new HashSet<>();
            }
            clusters.add(c);
        }

        // Pruning Clusters
        if (clusters.size() > n) {
            pruneCluster(clusters.size() - n);
        }

        // Making .txt Files
        makeTextFiles();
    }

    public static List<Point> findNeighbor(Point point) {
        List<Point> pointList = new ArrayList<>();
        for (Point p : db) {
            double distance = Math.sqrt(Math.pow((point.x - p.x), 2) + Math.pow((point.y - p.y), 2));
            if (distance <= Eps) {
                pointList.add(p);
            }
        }

        return pointList;
    }

    public static void pruneCluster(int count) {
        while (count > 0) {
            int clusterID = -1;
            int min = Integer.MAX_VALUE;
            for (Cluster c : clusters) {
                if (c.pointList.size() < min) {
                    min = c.pointList.size();
                    clusterID = c.id;
                }
            }
            for (Cluster c : clusters) {
                if (c.id == clusterID) {
                    clusters.remove(c);
                    break;
                }
            }
            count--;
        }
    }

    public static void makeTextFiles() throws Exception {
        int idx = -1;
        for (Cluster cluster : clusters) {
            File file = new File("input" + String.valueOf(inputNum) + "_cluster_" + String.valueOf(++idx) + ".txt");
            file.createNewFile();
            FileWriter fw = new FileWriter(file);
            BufferedWriter writer = new BufferedWriter(fw);

            for (Point point : cluster.pointList) {
                writer.write(String.valueOf(point.id) + "\n");
            }

            writer.close();
        }
    }
}
