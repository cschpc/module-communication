#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

int dgemm_(char *transa, char *transb, int *m, int * n,
           int *k, double *alpha, double *a, int *lda,
           double *b, int *ldb, double *beta,
           double *c, int *ldc);


int main(int argc, char *argv[])
{
  int n;
  
  // matrices
  double *a, *b, *c;

  char trans = 'n';
  double alpha = 1.0;
  double beta = 0.0;

  size_t matsize, ind;
  

  assert(argc == 2);
  n = atoi(argv[1]);

  matsize = n * n;

  a = (double* ) malloc(matsize * sizeof(double));
  if (a == NULL) {
    printf("%d x %d matrix a could not be allocated\n", n, n);
    exit(-1);
  }
  b = (double* ) malloc(matsize * sizeof(double));
  if (b == NULL) {
    printf("%d x %d matrix b could not be allocated\n", n, n);
    exit(-1);
  }
  c = (double* ) malloc(matsize * sizeof(double));
  if (c == NULL) {
    printf("%d x %d matrix c could not be allocated\n", n, n);
    exit(-1);
  }

  // fill values
  for (int i=0; i < n; i++) {
    for (int j=0; j < n; j++) {
      ind = i; // in order to protect from integer overflow index is calculated in parts
      ind *= n;
      ind += j;
      a[ind] = i*10.0 + j;
      b[ind] = i - j*20.0;
    }
  }

  dgemm_(&trans, &trans, &n, &n, &n, &alpha, a, &n, b, &n, &beta, c, &n); 

  free(a);
  free(b);
  free(c);

  return(0);
}


