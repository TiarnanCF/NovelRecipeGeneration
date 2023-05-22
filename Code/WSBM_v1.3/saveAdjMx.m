function [labels,model] = saveAdjMx(regions,alpha,beta)

    %Construct adjacency matrix
    number = length(regions);
    adjMx = zeros(1033*number);
    for i = 1:number
        for j=1:number
            adjMx((1 + 1033*(i-1)):(1033*(i)),(1 + 1033*(j-1)):(1033*(j))) = beta .* eye(1033);
        end
    end

    %Load in matrix from saved files
    for i = 1:number
        newMx = readmatrix(strcat('..\adjMx\adjMx',string(regions(i)),'.txt'));
        adjMx((1 + 1033*(i-1)):(1033*(i)),(1 + 1033*(i-1)):(1033*(i))) = newMx;
    end
    
    %Set non-edges to "NaN"
    adjMx(adjMx == 0) = nan;
    %Subtract one from each edge weight
    adjMx = adjMx - 1;
    
    %Run WSBM
    [labels,model] = wsbm(adjMx ,10,'W_Distr','Poisson','alpha',alpha,'numTrials',12,'parallel',1);
    
    %Save data
    thetaW = reshape(model.Para.tau_w(:,1),10,10);
    thetaE = reshape(model.Para.theta_e,10,10);
    
    writematrix(thetaW, strcat('..\params\thetaW',string(beta),'.txt'))
    writematrix(thetaE, strcat('..\params\thetaE',string(beta),'.txt'))
    writematrix(labels,strcat('..\params\z',string(beta),'.txt'))
    writematrix(regions,strcat('..\params\regions',string(beta),'.txt'))
end
