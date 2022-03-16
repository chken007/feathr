from feathr.anchor import FeatureAnchor
from feathr.feature import Feature
from feathr.source import HdfsSource
from feathr.dtype import BOOLEAN, INT32, FLOAT, ValueType
from feathr.source import PASSTHROUGH_SOURCE
from feathr.transformation import WindowAggTransformation
from feathr.typed_key import TypedKey

def test_request_feature_anchor_to_config():
    features = [
        Feature(name="trip_distance", feature_type=FLOAT),
        Feature(name="f_is_long_trip_distance",
                feature_type=BOOLEAN,
                transform="cast_float(trip_distance)>30"),
        Feature(name="f_day_of_week",
                feature_type=INT32,
                transform="dayofweek(lpep_dropoff_datetime)")
    ]

    anchor = FeatureAnchor(name="request_features",
                           source=PASSTHROUGH_SOURCE,
                           features=features)
    expected_non_agg_feature_config = """
           request_features: {
               source: PASSTHROUGH
               key: [NOT_NEEDED]
               features: {
                    trip_distance: {
                        def: "trip_distance"
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: FLOAT
                        }
                    } 
                    f_is_long_trip_distance: {
                        def: "cast_float(trip_distance)>30"
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: BOOLEAN
                        } 
                    } 
                    f_day_of_week: { 
                        def:"dayofweek(lpep_dropoff_datetime)"
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: INT
                        }
                    }
               }
           }
    """
    assert ''.join(anchor.to_feature_config().split()) == ''.join(expected_non_agg_feature_config.split())


def test_non_agg_feature_anchor_to_config():
    batch_source = HdfsSource(name="nycTaxiBatchSource",
                              path="abfss://feathrazuretest3fs@feathrazuretest3storage.dfs.core.windows.net/demo_data/green_tripdata_2020-04.csv",
                              event_timestamp_column="lpep_dropoff_datetime",
                              timestamp_format="yyyy-MM-dd HH:mm:ss")

    location_id = TypedKey(key_column="DOLocationID",
                     key_column_type=ValueType.INT32,
                     description="location id in NYC",
                     full_name="nyc_taxi.location_id")
    features = [
        Feature(name="f_loc_is_long_trip_distance",
                feature_type=BOOLEAN,
                transform="cast_float(trip_distance)>30", key=location_id),
        Feature(name="f_loc_day_of_week",
                feature_type=INT32,
                transform="dayofweek(lpep_dropoff_datetime)", key=location_id)
    ]

    anchor = FeatureAnchor(name="nonAggFeatures",
                           source=batch_source,
                           features=features)
    expected_non_agg_feature_config = """
           nonAggFeatures: {
               source: nycTaxiBatchSource
               key: [DOLocationID]
               features: {
                    f_loc_is_long_trip_distance: {
                        def: "cast_float(trip_distance)>30"
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: BOOLEAN
                        } 
                    } 
                    f_loc_day_of_week: { 
                        def:"dayofweek(lpep_dropoff_datetime)"
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: INT
                        }
                    }
               }
           }
    """
    assert ''.join(anchor.to_feature_config().split()) == ''.join(expected_non_agg_feature_config.split())


def test_agg_anchor_to_config():
    batch_source = HdfsSource(name="nycTaxiBatchSource",
                              path="abfss://feathrazuretest3fs@feathrazuretest3storage.dfs.core.windows.net/demo_data/green_tripdata_2020-04.csv",
                              event_timestamp_column="lpep_dropoff_datetime",
                              timestamp_format="yyyy-MM-dd HH:mm:ss")

    location_id = TypedKey(key_column="DOLocationID",
                     key_column_type=ValueType.INT32,
                     description="location id in NYC",
                     full_name="nyc_taxi.location_id")
    agg_features = [Feature(name="f_location_avg_fare",
                            key=location_id,
                            feature_type=FLOAT,
                            transform=WindowAggTransformation(agg_expr="cast_float(fare_amount)",
                                                         agg_func="AVG",
                                                         window="90d")),
                    Feature(name="f_location_max_fare",
                            key=location_id,
                            feature_type=FLOAT,
                            transform=WindowAggTransformation(agg_expr="cast_float(fare_amount)",
                                                         agg_func="MAX",
                                                         window="90d"))
                    ]
    
    agg_anchor = FeatureAnchor(name="aggregationFeatures",
                               source=batch_source,
                               features=agg_features)

    expected_agg_feature_config = """
            aggregationFeatures: {
                source: nycTaxiBatchSource
                key: [DOLocationID]
                features: {
                    f_location_avg_fare: {
                        def: "cast_float(fare_amount)"
                        window: 90d
                        agg: AVG
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: FLOAT
                        }
                    }
                    f_location_max_fare: {
                        def: "cast_float(fare_amount)"
                        window: 90d
                        agg: MAX
                        type: {
                            type: TENSOR
                            tensorCategory: DENSE
                            dimensionType: []
                            valType: FLOAT
                        }
                    }
                }
            }
        """
    assert ''.join(agg_anchor.to_feature_config().split()) == ''.join(expected_agg_feature_config.split())