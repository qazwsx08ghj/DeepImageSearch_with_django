from .serializers import ImageSerializer
from .models import Image
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from annoy import AnnoyIndex
from DeepImageSearch import LoadData, Index, SearchImage
from DeepImageSearch.DeepImageSearch import FeatureExtractor
import DeepImageSearch.config as config
from PIL import Image as pl_Image
import pandas as pd

# Create your views here.


class ByteStringSearch(SearchImage):

    def __init__(self):
        self.image_data = pd.read_pickle(config.image_data_with_features_pkl)
        self.f = len(self.image_data['features'][0])

    def search_by_vector(self, v, n: int):
        v = v  # Feature Vector
        n = n  # number of output
        u = AnnoyIndex(self.f, 'euclidean')
        u.load(config.image_features_vectors_ann)
        index_list = u.get_nns_by_vector(v, n)  # will find the 10 nearest neighbors
        return dict(zip(index_list, self.image_data.iloc[index_list]['images_paths'].to_list()))

    def get_query_vector(self, byte_string_image):
        img = pl_Image.open(byte_string_image)
        fe = FeatureExtractor()
        query_vector = fe.extract(img)
        return query_vector

    def get_similar_images(self, byte_string_image, number_of_images: int):
        query_vector = self.get_query_vector(byte_string_image=byte_string_image)
        img_dict = self.search_by_vector(query_vector, number_of_images)
        return img_dict


class ImageViewSet(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, requset, *args, **kwargs):
        file = requset.FILES['image']
        httpResponse = {"search Response": None}
        search = ByteStringSearch().get_similar_images(file, 5)
        if search:
            httpResponse = {"search Response": 'success'}
        Image.objects.create(image=file)
        httpResponse.update(search)
        return Response(httpResponse)
