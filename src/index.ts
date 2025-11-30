import { Container, getContainer } from "@cloudflare/containers";
import { Hono } from "hono";

export class JReviewsContainer extends Container<Env> {
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
			USE_GMB_OAUTH: env.USE_GMB_OAUTH,
			GMB_CLIENT_ID: env.GMB_CLIENT_ID,
			GMB_CLIENT_SECRET: env.GMB_CLIENT_SECRET,
			GMB_REFRESH_TOKEN: env.GMB_REFRESH_TOKEN,
			GMB_ACCOUNT_ID: env.GMB_ACCOUNT_ID,
			GMB_LOCATION_ID: env.GMB_LOCATION_ID,
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

// Proxy all requests to the container
app.all("/*", async (c) => {
	// Use a singleton to ensure we always get the same container instance
	const container = getContainer(c.env.GOOGLE_REVIEWS_CONTAINER, "fetcher");
	// Forward the request to the container
	return await container.fetch(c.req.raw);
});

export default app;
