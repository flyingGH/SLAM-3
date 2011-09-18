% Read data from file
data = getData('sim4');

% Load Constants
Constants

% Get Initial Distribution
chi = GenerateInitialDistribution();

dataSize = size(data);

result = zeros(6,dataSize(1));

for X = 1:dataSize(1)
    u = [data(X,4);data(X,5)];
    z = [data(X,2);data(X,3);data(X,6);data(X,7);data(X,8);data(X,9)];
    chi = ParticleFilter(chi,u,z);
    result(:,X) = mean(chi,2);
    X
end

clf
scatter(result(1,:), result(2,:))
hold on
scatter(data(:,10), data(:,11), 'r')