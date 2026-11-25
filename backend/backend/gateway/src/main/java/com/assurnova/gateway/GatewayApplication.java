package com.assurnova.gateway;

import com.assurnova.gateway.loadbalancer.RandomLoadBalancerConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;

@EnableDiscoveryClient
@SpringBootApplication
@LoadBalancerClient(
        name = "candidat",
        configuration = RandomLoadBalancerConfig.class
)
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}