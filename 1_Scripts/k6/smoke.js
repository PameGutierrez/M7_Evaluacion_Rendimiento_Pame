// k6 - Prueba de humo para endpoints públicos (reqres.in)
import http from 'k6/http';
import { sleep, check } from 'k6';
export const options = {
  vus: 5,
  duration: '30s'
};
export default function () {
  let res1 = http.get('https://reqres.in/api/users?page=2');
  check(res1, {'GET lista 200': (r) => r.status === 200});
  let res2 = http.get('https://reqres.in/api/users/2');
  check(res2, {'GET usuario 200': (r) => r.status === 200});
  let loginPayload = JSON.stringify({ email: 'eve.holt@reqres.in', password: 'cityslicka' });
  let headers = { 'Content-Type': 'application/json' };
  let res3 = http.post('https://reqres.in/api/login', loginPayload, { headers });
  check(res3, {'POST login 200/OK': (r) => r.status === 200});
  sleep(1);
}
