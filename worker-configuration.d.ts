interface Env {
    GOOGLE_API_KEY: string;
    PLACE_ID: string;
    USE_GMB_OAUTH: string;
    GMB_CLIENT_ID: string;
    GMB_CLIENT_SECRET: string;
    GMB_REFRESH_TOKEN: string;
    GMB_ACCOUNT_ID: string;
    GMB_LOCATION_ID: string;
    GOOGLE_REVIEWS_CONTAINER: DurableObjectNamespace<import("./src/index").JReviewsContainer>;
}
