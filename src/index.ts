import { Container, getContainer } from "@cloudflare/containers";
import { Hono } from "hono";

export class GoogleReviewsContainer extends Container<Env> {
	// Port the container listens on (default: 8080)
	defaultPort = 8080;
	// Time before container sleeps due to inactivity (default: 30s)
	sleepAfter = "2m";

	// Environment variables passed to the container
	envVars: Record<string, string>;

	constructor(state: any, env: Env) {
		super(state, env);
		this.envVars = {
			GOOGLE_API_KEY: env.GOOGLE_API_KEY,
			PLACE_ID: env.PLACE_ID,
			OUTPUT_FILE: "/data/reviews.json"
		};
	}

	// Optional lifecycle hooks
	override onStart() {
		console.log("Google Reviews Container successfully started");
	}

	override onStop() {
		console.log("Google Reviews Container successfully shut down");
	}

	override onError(error: unknown) {
		console.log("Container error:", error);
	}
}

// Create Hono app with proper typing for Cloudflare Workers
const app = new Hono<{
	Bindings: Env;
}>();

// Home route
app.get("/", async (c) => {
	// Use a singleton to ensure we always get the same container instance
	const container = getContainer(c.env.GOOGLE_REVIEWS_CONTAINER, "fetcher");
	// Forward the request to the container
	return await container.fetch(c.req.raw);
});

export default app;
