# Use the official Redis image from the Docker Hub
FROM redis:latest

# Add Redis configuration file
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose the default Redis port
EXPOSE 6379

# Set the entrypoint to the Redis server with the custom configuration
ENTRYPOINT ["redis-server", "/usr/local/etc/redis/redis.conf"]

