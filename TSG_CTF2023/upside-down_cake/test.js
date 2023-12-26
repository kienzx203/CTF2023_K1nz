import { serve } from '@hono/node-server';
import { serveStatic } from '@hono/node-server/serve-static';
import { Hono } from 'hono';

const flag = process.env.FLAG ?? 'DUMMY{DUMMY}';

const validatePalindrome = (string) => {
	if (string.length < 1000) {
		console.log(string.length);
		return 'too short';
	}
	console.log(string);
	console.log(string.length);
	console.log(Array(string.length).keys());
	console.log(Array(string.length));
	for (const i of Array(string.length).keys()) {
		console.log(i);
		const original = string[i];
		console.log(original);
		console.log(string.length - i - 1)
		const reverse = string[string.length - i - 1];
		console.log(reverse);
		console.log(typeof original);
		if (original !== reverse || typeof original !== 'string') {
			return 'not palindrome';
		}
	}
	return null;
}

const app = new Hono();

app.get('/', serveStatic({ root: '.' }));

app.post('/', async (c) => {
	const { palindrome } = await c.req.json();
	console.log(palindrome);
	const error = validatePalindrome(palindrome);
	if (error) {
		c.status(400);
		return c.text(error);
	}
	return c.text(`I love you! Flag is ${flag}`);
});

app.port = 12349;

serve(app);