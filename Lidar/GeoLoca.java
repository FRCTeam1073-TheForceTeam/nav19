
public class Location {

    public void geoLoca(){

    }
    public double latitude(){

    }
    public double longitude(){

    }

    public Location(String geoLoca, double latitude, double longitude) {
            this.geoLoca = geoLoca;
            this.latitude = latitude;
            this.longitude = longitude;
    }
}

public class Route {

    public Location[] waypoints;

    public Route(Location... waypoints) {
        this.waypoints = waypoints;
    }
}

public class geoAssist {

    public static double calcGeoDistanceInInches(double lat1, double lat2, double lon1, double lon2){
        double dlat = math.abs(lat1-lat2);
        double dlon = math.abs(lon1 - lon2);
        double a = math.pow((math.sin(dlat/2)), 2) + Math.cos(lat1);
    }
}
