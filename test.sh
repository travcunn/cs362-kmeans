for i in ../image-library/*; do
for k in 'seq 3 10'; do # process the images with k=3 to 10
cat $i | convert - -colorspace gray -compress none -depth 8 pgm:- | ./kmean-simple $k | convert - result_simple_${k}_$(basename $i)
cat $i | convert - -colorspace gray -compress none -depth 8 pgm:- | ./kmean-prob $k | convert - result_prob_${k}_$(basename $i)
done
done
