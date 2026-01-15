
x = 0;
y = zeros(5);
z = x + y;

x = eye(5);
y = eye(8);
z = x + y;

x = [ 1,2,3,4,5 ];
y = [ 1,2,3,4,5;
      1,2,3,4,5 ];
z = x + y;

x = zeros(5);
y = zeros(7);
z = x + yyyy; #//TODO: Fix unknown variable

x = ones(3); #//TODO: Fix this exception
z = x[10, 1]; #//TODO: Fix those indices
v = x[2];