import random
import math

def train_test_split(X, y, test_size=0.2, random_state=42):
    n_test = int(len(X) * test_size)
    indices = list(range(len(X)))
    random.seed(random_state)
    random.shuffle(indices)
    X_train = [X[i] for i in indices[:-n_test]]
    X_test = [X[i] for i in indices[-n_test:]]
    y_train = [y[i] for i in indices[:-n_test]]
    y_test = [y[i] for i in indices[-n_test:]]
    return X_train, X_test, y_train, y_test

class KNeighborsRegressor:
    def __init__(self, n_neighbors=5, weights='distance'):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = []
        for x in X:
            distances = [math.sqrt(sum((x_i - xi) ** 2 for x_i, xi in zip(x, x_train))) for x_train in self.X_train]
            nearest_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:self.n_neighbors]
            nearest_distances = [distances[i] for i in nearest_indices]
            nearest_labels = [self.y_train[i] for i in nearest_indices]
            if self.weights == 'distance':
                weights = [1 / (d + 1e-5) for d in nearest_distances]
                prediction = sum(nl * w for nl, w in zip(nearest_labels, weights)) / sum(weights)
            else:
                prediction = sum(nearest_labels) / len(nearest_labels)
            predictions.append(prediction)
        return predictions

def mean_absolute_error(y_true, y_pred):
    return sum(abs(y_t - y_p) for y_t, y_p in zip(y_true, y_pred)) / len(y_true)

def generate_data(n_samples=1000, n_sensors=5):
    random.seed(42)
    angles = [random.uniform(0, 360) for _ in range(n_samples)]  # Angles in degrees
    distances = [[abs(math.sin(math.radians(angle) + random.uniform(-0.1, 0.1))) for _ in range(n_sensors)] for angle in angles]
    return distances, angles

distances, angles = generate_data()
X_train, X_test, y_train, y_test = train_test_split(distances, angles, test_size=0.2, random_state=42)

k = 5  # Number of neighbors
knn = KNeighborsRegressor(n_neighbors=k, weights='distance')
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} degrees")

demo_input = [X_test[0]]
predicted_angle = knn.predict(demo_input)
print(f"Predicted angle: {predicted_angle[0]:.2f} degrees")
