interface Env {
    GOOGLE_API_KEY: string;
    PLACE_ID: string;
    GOOGLE_REVIEWS_CONTAINER: DurableObjectNamespace<import("./src/index").GoogleReviewsContainer>;
}
