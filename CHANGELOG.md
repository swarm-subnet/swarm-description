# Changelog

## 1.0.0

- Every drone the Swarm simulator flies, one folder each: the DJI Matrice 4TD, the Crazyflie 2.x (cf2x), the Ryze Tello and the 36 cm interceptor. Each folder holds the drone's URDFs, its meshes, a `params.toml` with the source of every value, and a README.
- `drones()`, `drone_dir()`, `get_urdf()`, `get_params()` and `get_properties()` load them.
