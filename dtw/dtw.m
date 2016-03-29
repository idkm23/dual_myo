function [Dist,D,k,p]=dtw(s,t, w)
%Dynamic Time Warping Algorithm
%Dist is unnormalized distance between t and r
%D is the accumulated distance matrix
%k is the normalizing factor
%p is the optimal path
%s is the vector you are testing against
%t is the vector you are testing
%

if nargin<3
    w=Inf;
end

ns=size(s,1);
nt=size(t,1);
if size(s,2)~=size(t,2)
    error('Error in dtw(): the dimensions of the two input signals do not match.');
end
w=max(w, abs(ns-nt)); % adapt window size

%% initialization
D=zeros(ns+1,nt+1)+Inf; % cache matrix
D(1,1)=0;

%% begin dynamic programming
for i=1:ns
    for j=max(i-w,1):min(i+w,nt)
        oost=norm(s(i,:)-t(j,:));
        D(i+1,j+1)=oost+min( [D(i,j+1), D(i+1,j), D(i,j)] );
        
    end
end
d=D(ns+1,nt+1);

Dist=D(ns,nt);
n=ns;
m=nt;
k=1;
p=[];
p(1,:)=[ns,nt];
while ((n+m)~=2)
    if (n-1)==0
        m=m-1;
    elseif (m-1)==0
        n=n-1;
    else 
      [values,number]=min([D(n-1,m),D(n,m-1),D(n-1,m-1)]);
      switch number
      case 1
        n=n-1;
      case 2
        m=m-1;
      case 3
        n=n-1;
        m=m-1;
      end
  end
    k=k+1;
    p=cat(1,p,[n,m]);
end

