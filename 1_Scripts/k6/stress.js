// k6 - Prueba de estrés con etapas
import http from 'k6/http';
import { sleep, check } from 'k6';
export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '45s', target: 30 },
    { duration: '45s', target: 50 },
    { duration: '1m', target: 0 }
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'], // p95 bajo 800ms
    http_req_failed: ['rate<0.05']    // error rate &lt; 5%
  }
};
export default function () {
  const responses = http.batch([
    ['GET', 'https://reqres.in/api/users?page=2'],
    ['GET', 'https://reqres.in/api/users/2']
  ]);
  for (const r of responses) {
    check(r, {'status 200': (x) => x.status === 200});
  }
  sleep(1);
}
