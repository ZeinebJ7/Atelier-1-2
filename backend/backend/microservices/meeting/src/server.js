
const { Eureka } = require('eureka-js-client');
const app = require('./app');

const PORT = process.env.PORT || 8083;

const client = new Eureka({
  instance: {
    app: 'MEETING',
      instanceId: `meeting:localhost:${PORT}`,
    hostName: 'localhost',
    ipAddr: '127.0.0.1',
      statusPageUrl: `http://localhost:${PORT}/swagger-ui`,
    port: {
      '$': PORT,
      '@enabled': true
    },
    vipAddress: 'meeting',
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },
  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/'
  }
});

app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  client.start((error) => {
    if (error) {
      console.error('Eureka registration failed:', error);
    } else {
      console.log('MEETING successfully registered with Eureka!');
    }
  });
});

process.on('SIGINT', () => {
  client.stop();
  process.exit();
});
