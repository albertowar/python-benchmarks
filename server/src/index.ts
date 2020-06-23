import * as express from 'express';

const app = express();



app.get('/text', (_: express.Request, response: express.Response) => {
  response.send('Hello world!');
});

app.get('/json', (_: express.Request, response: express.Response) => {
    response.json({ 'message': 'Hello world!' });
});

const PORT: number = Number(process.env.PORT || 3000);
app.listen(PORT, () => {
    console.log(`Running on port ${PORT}`);
});